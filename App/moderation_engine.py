from App.classifier import NSFWDetector
from App.text_moderator.text_moderator import TextModerator
from App.video_moderator.video_moderator import VideoModerator
from App.logger import logger


class ModerationEngine:
    """
    Central moderation orchestrator with logging
    """

    def __init__(self):
        self.image_moderator = NSFWDetector()
        self.text_moderator = TextModerator()
        self.video_moderator = VideoModerator()

        logger.info("ModerationEngine initialized")

    def moderate_image(self, image_path: str):
        logger.info("IMAGE moderation started")

        try:
            result = self.image_moderator.classify(image_path)
            logger.info(
                f"IMAGE verdict={result.get('verdict')} "
                f"confidence={max(result.get('sexual_score', 0.0), result.get('soft_score', 0.0))}"
            )
            return result

        except Exception as e:
            logger.error(f"IMAGE moderation failed: {str(e)}")
            raise

    def moderate_text(self, text: str):
        logger.info("TEXT moderation started")

        try:
            result = self.text_moderator.classify(text)
            logger.info(
                f"TEXT verdict={result.get('verdict')} "
                f"confidence={result.get('confidence')}"
            )
            return result

        except Exception as e:
            logger.error(f"TEXT moderation failed: {str(e)}")
            raise

    def moderate_video(self, video_path: str):
        logger.info("VIDEO moderation started")

        try:
            result = self.video_moderator.classify(video_path)
            logger.info(
                f"VIDEO verdict={result.get('verdict')} "
                f"confidence={result.get('confidence')}"
            )
            return result

        except Exception as e:
            logger.error(f"VIDEO moderation failed: {str(e)}")
            raise
