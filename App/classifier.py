from nudenet import NudeDetector

class NSFWDetector:
    def __init__(self):
        self.detector = NudeDetector()

    def classify(self, image_path):
        detections = self.detector.detect(image_path)

        sexual_parts = {
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_EXPOSED",
            "FEMALE_BREAST_EXPOSED"
        }

        soft_parts = {
            "MALE_CHEST",
            "FEMALE_BREAST_COVERED",
            "BELLY_EXPOSED",
            "ARMPITS_EXPOSED",
            "TORSO_EXPOSED"
        }

        sexual_score = 0.0
        soft_score = 0.0

        for d in detections:
            label = d.get("class", "")
            score = float(d.get("score", 0))

            if label in sexual_parts and score >= 0.5:
                sexual_score += score

            elif label in soft_parts and score >= 0.6:
                soft_score += score

        # 🚫 Explicit NSFW
        if sexual_score >= 0.7:
            return {
                "verdict": "NSFW",
                "reason": "Explicit sexual content detected"
            }

        # ✅ Saree / Gym / Beach safe downgrade
        if sexual_score == 0 and soft_score <= 1.2:
            return {
                "verdict": "SAFE",
                "reason": "Non-sexual skin exposure"
            }

        # ⚠️ Only ambiguous cases
        return {
            "verdict": "REVIEW",
            "reason": "Ambiguous skin exposure"
        }
