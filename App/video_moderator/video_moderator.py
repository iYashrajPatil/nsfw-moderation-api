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

        self.FRAME_INTERVAL_SEC = 2.0
        self.NSFW_RATIO_THRESHOLD = 0.3
        self.REVIEW_RATIO_THRESHOLD = 0.1

    def classify(self, video_path: str) -> Dict:
        logger.info(f"Starting video moderation: {os.path.basename(video_path)}")

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_interval = int(fps * self.FRAME_INTERVAL_SEC)

        total_frames = 0
        nsfw_frames = 0
        review_frames = 0
        max_confidence = 0.0

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

                # 🔑 USE IMAGE SCORES DIRECTLY
                frame_confidence = max(
                    result.get("sexual_score", 0.0),
                    result.get("soft_score", 0.0)
                )

                max_confidence = max(max_confidence, frame_confidence)

                if verdict == "NSFW":
                    nsfw_frames += 1
                    logger.warning(
                        f"NSFW frame detected | frame={total_frames} | conf={frame_confidence:.2f}"
                    )

                elif verdict == "REVIEW":
                    review_frames += 1
                    logger.info(
                        f"REVIEW frame detected | frame={total_frames} | conf={frame_confidence:.2f}"
                    )

                # 🚀 EARLY EXIT
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
                "confidence": 0.0
            }

        nsfw_ratio = nsfw_frames / total_frames
        review_ratio = review_frames / total_frames

        if nsfw_ratio >= self.NSFW_RATIO_THRESHOLD:
            verdict = "NSFW"
        elif review_ratio >= self.REVIEW_RATIO_THRESHOLD:
            verdict = "REVIEW"
        else:
            verdict = "SAFE"

        logger.info(
            f"Final verdict={verdict} | "
            f"nsfw_ratio={nsfw_ratio:.2f} | "
            f"max_confidence={max_confidence:.2f}"
        )

        return {
            "type": "video",
            "verdict": verdict,
            "confidence": round(max_confidence, 2)
        }
