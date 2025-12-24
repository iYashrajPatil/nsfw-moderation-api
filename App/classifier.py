import os
from typing import Dict, List


class NSFWDetector:
    """
    Lightweight NSFW moderation logic using NudeNet
    Model is loaded lazily (only when first image is classified)
    """

    def __init__(self):
        self.detector = None

        # Explicit sexual content
        self.explicit_parts = {
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_EXPOSED",
            "FEMALE_BREAST_EXPOSED"
        }

        # Soft / suggestive content
        self.soft_parts = {
            "FEMALE_BREAST_COVERED",
            "MALE_CHEST",
            "BELLY_EXPOSED",
            "TORSO_EXPOSED",
            "ARMPITS_EXPOSED",
            "BUTTOCKS_EXPOSED"
        }

        # Thresholds
        self.EXPLICIT_THRESHOLD = 0.7
        self.SOFT_SINGLE_IGNORE = 0.6
        self.SOFT_CUMULATIVE_SAFE = 1.2

    def _load_model(self):
        """Load NudeNet model only once"""
        if self.detector is None:
            from nudenet import NudeDetector
            self.detector = NudeDetector()

    def classify(self, image_path: str) -> Dict:
        """
        Classify image into SAFE / NSFW / REVIEW
        """
        self._load_model()

        detections: List[Dict] = self.detector.detect(image_path)

        if not detections:
            return {"verdict": "SAFE", "reason": "No detections"}

        sexual_score = 0.0
        soft_score = 0.0

        for det in detections:
            label = det.get("class", "")
            score = float(det.get("score", 0.0))

            if label in self.explicit_parts and score >= 0.5:
                sexual_score += score

            elif label in self.soft_parts and score >= self.SOFT_SINGLE_IGNORE:
                soft_score += score

        if sexual_score >= self.EXPLICIT_THRESHOLD:
            return {
                "verdict": "NSFW",
                "sexual_score": sexual_score
            }

        if sexual_score == 0 and soft_score <= self.SOFT_CUMULATIVE_SAFE:
            return {
                "verdict": "SAFE",
                "soft_score": soft_score
            }

        return {
            "verdict": "REVIEW",
            "sexual_score": sexual_score,
            "soft_score": soft_score
        }
