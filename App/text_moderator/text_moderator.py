from typing import Dict
import re
import joblib
import os
import logging

# ----------------------------
# Logger setup
# ----------------------------
logger = logging.getLogger("text_moderator")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [TEXT] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class TextModerator:
    """
    Production-ready text moderation (social-media focused)

    Combines:
    - Rule-based explicit keyword handling
    - ML probability (TF-IDF + Logistic Regression)

    Verdicts:
    SAFE | REVIEW | NSFW
    """

    def __init__(self):
        # 🔴 Strong sexual words (never SAFE)
        self.explicit_words = {
            "sex", "porn", "fuck", "blowjob", "handjob",
            "pussy", "dick", "xxx", "nude"
        }

        # 🟠 Abusive / borderline
        self.abusive_words = {
            "bitch", "slut", "whore", "bastard", "shit"
        }

        # Thresholds
        self.NSFW_THRESHOLD = 0.75
        self.REVIEW_THRESHOLD = 0.35

        # ML
        self.model = None
        self.vectorizer = None
        self._load_ml_model()

    def _load_ml_model(self):
        try:
            base_dir = os.path.dirname(__file__)
            model_path = os.path.join(base_dir, "..", "models", "text_model.pkl")
            vec_path = os.path.join(base_dir, "..", "models", "tfidf.pkl")

            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vec_path)
            logger.info("ML text model loaded")

        except Exception:
            logger.warning("ML model not found — rule-based only")

    def _rule_score(self, text: str) -> float:
        words = re.findall(r"\w+", text.lower())

        explicit_hits = sum(1 for w in words if w in self.explicit_words)
        abusive_hits = sum(1 for w in words if w in self.abusive_words)

        # 🚨 Hard boost for explicit sexual content
        if explicit_hits >= 1:
            return 0.6 + (explicit_hits * 0.2)

        return abusive_hits * 0.25

    def _ml_score(self, text: str) -> float:
        if not self.model or not self.vectorizer:
            return 0.0

        vec = self.vectorizer.transform([text])
        return float(self.model.predict_proba(vec)[0][1])

    def classify(self, text: str) -> Dict:
        rule_score = self._rule_score(text)
        ml_score = self._ml_score(text)

        confidence = max(rule_score, ml_score)

        # 🧠 Verdict logic
        if confidence >= self.NSFW_THRESHOLD:
            verdict = "NSFW"
        elif confidence >= self.REVIEW_THRESHOLD:
            verdict = "REVIEW"
        else:
            verdict = "SAFE"

        logger.info(
            f"Verdict={verdict} | rule={rule_score:.2f} | ml={ml_score:.2f}"
        )

        return {
            "type": "text",
            "verdict": verdict,
            "confidence": round(confidence, 2)
        }
