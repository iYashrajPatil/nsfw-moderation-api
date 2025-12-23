from nudenet import NudeDetector
import os


class NSFWDetector:
    def __init__(self):
        """
        Load NudeNet detector using a locally shipped ONNX model.
        This avoids auto-download issues on cloud platforms like Render.
        """

        # Absolute path to models/detector.onnx
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "..", "models", "detector.onnx")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"NudeNet model not found at {model_path}. "
                "Make sure detector.onnx is committed to the repo."
            )

        # ✅ Explicit model loading (Render-safe)
        self.detector = NudeDetector(model_path=model_path)

        # 🚫 Strong sexual indicators (always serious)
        self.sexual_parts = {
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_EXPOSED",
            "FEMALE_BREAST_EXPOSED"
        }

        # ⚠️ Context-dependent / clothing-related exposure
        self.soft_parts = {
            "FEMALE_BREAST_COVERED",
            "MALE_CHEST",
            "BELLY_EXPOSED",
            "TORSO_EXPOSED",
            "ARMPITS_EXPOSED",
            "BUTTOCKS_EXPOSED"
        }

        # 🧠 Thresholds (easy to tune later)
        self.EXPLICIT_THRESHOLD = 0.70
        self.SOFT_SINGLE_IGNORE = 0.60
        self.SOFT_CUMULATIVE_SAFE = 1.20
        self.REVIEW_LOWER_BOUND = 0.40

    def classify(self, image_path):
        detections = self.detector.detect(image_path)

        if not detections:
            return {
                "verdict": "SAFE",
                "reason": "No human skin patterns detected"
            }

        sexual_score = 0.0
        soft_score = 0.0
        explicit_hits = 0
        soft_hits = 0
        detailed_hits = []

        # 🔍 Analyze detections
        for d in detections:
            label = d.get("class", "")
            score = float(d.get("score", 0.0))

            # Explicit sexual content
            if label in self.sexual_parts and score >= 0.5:
                sexual_score += score
                explicit_hits += 1
                detailed_hits.append((label, score))

            # Soft / contextual exposure
            elif label in self.soft_parts and score >= self.SOFT_SINGLE_IGNORE:
                soft_score += score
                soft_hits += 1
                detailed_hits.append((label, score))

        # 🚫 HARD NSFW
        if explicit_hits >= 1 and sexual_score >= self.EXPLICIT_THRESHOLD:
            return {
                "verdict": "NSFW",
                "reason": "Explicit sexual anatomy detected",
                "signals": detailed_hits
            }

        # ✅ CLEAR SAFE (saree, gym, beach, traditional clothing)
        if explicit_hits == 0 and soft_score <= self.SOFT_CUMULATIVE_SAFE:
            return {
                "verdict": "SAFE",
                "reason": "Contextual or non-sexual skin exposure",
                "signals": detailed_hits
            }

        # ⚠️ REVIEW (edge cases)
        if (
            explicit_hits == 0
            and soft_score > self.SOFT_CUMULATIVE_SAFE
            and soft_score < (self.SOFT_CUMULATIVE_SAFE + 0.6)
        ):
            return {
                "verdict": "REVIEW",
                "reason": "Ambiguous skin exposure pattern",
                "signals": detailed_hits
            }

        # 🚫 Fallback
        return {
            "verdict": "REVIEW",
            "reason": "Uncertain detection confidence",
            "signals": detailed_hits
        }
