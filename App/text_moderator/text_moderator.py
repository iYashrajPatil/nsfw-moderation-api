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


class TextModerator:
    """
    Production-ready lightweight text moderation system.

    Combines:
    - Rule-based keyword scoring
    - ML-based probability (TF-IDF + Logistic Regression)

    Verdicts:
    SAFE | REVIEW | NSFW
    """

    def __init__(self):
        self.explicit_words = {
            "sex", "nude", "porn", "fuck", "blowjob", "handjob",
            "boobs", "pussy", "dick", "xxx"
        }

        self.abusive_words = {
            "bitch", "slut", "whore", "bastard", "shit"
        }

        self.NSFW_THRESHOLD = 0.75
        self.REVIEW_THRESHOLD = 0.4

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

            logger.info("Text ML model loaded successfully")

        except Exception:
            logger.warning("ML model not found — using rule-based only")

    def _rule_score(self, text: str) -> float:
        words = re.findall(r"\w+", text.lower())
        hits = sum(
            1 for w in words
            if w in self.explicit_words or w in self.abusive_words
        )
        return min(1.0, hits * 0.3)

    def _ml_score(self, text: str) -> float:
        if not self.model or not self.vectorizer:
            return 0.0

        vec = self.vectorizer.transform([text])
        return float(self.model.predict_proba(vec)[0][1])

    def classify(self, text: str) -> Dict:
        rule_score = self._rule_score(text)
        ml_score = self._ml_score(text)

        confidence = max(rule_score, ml_score)

        if confidence >= self.NSFW_THRESHOLD:
            verdict = "NSFW"
        elif confidence >= self.REVIEW_THRESHOLD:
            verdict = "REVIEW"
        else:
            verdict = "SAFE"

        logger.info(
            f"Text verdict={verdict} | rule={rule_score:.2f} | ml={ml_score:.2f}"
        )

        return {
            "type": "text",
            "verdict": verdict,
            "confidence": round(confidence, 2)
        }
