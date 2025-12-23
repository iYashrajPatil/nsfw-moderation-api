from nudenet import NudeDetector


class NSFWDetector:
    def __init__(self):
        # Load NudeNet detector (auto-downloads model internally)
        self.detector = NudeDetector()

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

        # 🚫 HARD NSFW (high confidence explicit exposure)
        if explicit_hits >= 1 and sexual_score >= self.EXPLICIT_THRESHOLD:
            return {
                "verdict": "NSFW",
                "reason": "Explicit sexual anatomy detected",
                "signals": detailed_hits
            }

        # ✅ CLEAR SAFE (saree, gym wear, beach, traditional clothing)
        if explicit_hits == 0 and soft_score <= self.SOFT_CUMULATIVE_SAFE:
            return {
                "verdict": "SAFE",
                "reason": "Contextual or non-sexual skin exposure",
                "signals": detailed_hits
            }

        # ⚠️ REVIEW (edge cases only)
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

        # 🚫 Fallback safety net
        return {
            "verdict": "REVIEW",
            "reason": "Uncertain detection confidence",
            "signals": detailed_hits
        }
