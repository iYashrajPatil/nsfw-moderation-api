import cv2
import os
import tempfile
from typing import Dict
import logging

from App.classifier import NSFWDetector


# ----------------------------
# Logger configuration
# ----------------------------
logger = logging.getLogger("video_moderator")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [VIDEO] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class VideoModerator:
    """
    Production-ready video moderation using frame sampling + ImageModerator
    """

    def __init__(self):
        self.detector = NSFWDetector()

        # Sampling config
        self.FRAME_INTERVAL_SEC = 2.0

        # Aggregation thresholds
        self.NSFW_RATIO_THRESHOLD = 0.3
        self.REVIEW_RATIO_THRESHOLD = 0.1

    def classify(self, video_path: str) -> Dict:
        logger.info(f"Starting video moderation: {os.path.basename(video_path)}")

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30
            logger.warning("FPS not detected, defaulting to 30")

        frame_interval = int(fps * self.FRAME_INTERVAL_SEC)

        total_frames = 0
        nsfw_frames = 0
        review_frames = 0
        confidences = []

        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_interval == 0:
                total_frames += 1

                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    temp_path = tmp.name
                    cv2.imwrite(temp_path, frame)

                result = self.detector.classify(temp_path)
                os.remove(temp_path)

                verdict = result.get("verdict", "SAFE")

                if verdict == "NSFW":
                    nsfw_frames += 1
                    confidence = max(
                        result.get("sexual_score", 0.8),
                        result.get("soft_score", 0.6)
                    )
                    logger.warning(f"NSFW frame detected (frame={total_frames})")

                elif verdict == "REVIEW":
                    review_frames += 1
                    confidence = 0.4
                    logger.info(f"REVIEW frame detected (frame={total_frames})")

                else:
                    confidence = 0.05

                confidences.append(confidence)

                # 🚀 Early exit
                if (
                    total_frames >= 5
                    and (nsfw_frames / total_frames) >= self.NSFW_RATIO_THRESHOLD
                ):
                    logger.warning("Early exit triggered due to NSFW ratio")
                    break

            frame_idx += 1

        cap.release()

        if total_frames == 0:
            logger.info("No frames processed — SAFE by default")
            return {
                "type": "video",
                "verdict": "SAFE",
                "confidence": 0.05
            }

        nsfw_ratio = nsfw_frames / total_frames
        review_ratio = review_frames / total_frames
        avg_conf = sum(confidences) / len(confidences)

        if nsfw_ratio >= self.NSFW_RATIO_THRESHOLD:
            verdict = "NSFW"
        elif review_ratio >= self.REVIEW_RATIO_THRESHOLD:
            verdict = "REVIEW"
        else:
            verdict = "SAFE"

        logger.info(
            f"Final verdict={verdict} | "
            f"nsfw_ratio={nsfw_ratio:.2f} | "
            f"confidence={avg_conf:.2f}"
        )

        return {
            "type": "video",
            "verdict": verdict,
            "confidence": round(avg_conf, 2)
        }
