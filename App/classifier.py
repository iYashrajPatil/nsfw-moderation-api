import os

# Force writable, fresh model directory (Render-safe)
os.environ["NUDENET_HOME"] = "/tmp/nudenet"


class NSFWDetector:
    def __init__(self):
        self.detector = None

        self.sexual_parts = {
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
        }

        self.soft_parts = {
            "FEMALE_BREAST_COVERED",
            "MALE_CHEST",
            "BELLY_EXPOSED",
            "TORSO_EXPOSED",
            "ARMPITS_EXPOSED",
            "BUTTOCKS_EXPOSED",
        }

        self.EXPLICIT_THRESHOLD = 0.7
        self.SOFT_SINGLE_IGNORE = 0.6
        self.SOFT_CUMULATIVE_SAFE = 1.2

    def _load_model(self):
        if self.detector is None:
            from nudenet import NudeDetector
            self.detector = NudeDetector()

    def classify(self, image_path: str):
        self._load_model()

        detections = self.detector.detect(image_path)

        if not detections:
            return {"verdict": "SAFE"}

        sexual_score = 0.0
        soft_score = 0.0

        for d in detections:
            label = d.get("class", "")
            score = float(d.get("score", 0.0))

            if label in self.sexual_parts and score >= 0.5:
                sexual_score += score

            elif label in self.soft_parts and score >= self.SOFT_SINGLE_IGNORE:
                soft_score += score

        if sexual_score >= self.EXPLICIT_THRESHOLD:
            return {"verdict": "NSFW"}

        if sexual_score == 0 and soft_score <= self.SOFT_CUMULATIVE_SAFE:
            return {"verdict": "SAFE"}

        return {"verdict": "REVIEW"}
