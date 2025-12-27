from App.video_moderator.video_moderator import VideoModerator

if __name__ == "__main__":
    moderator = VideoModerator()

    video_path = "sample_video.mp4"  # keep in project root
    result = moderator.classify(video_path)

    print("VIDEO RESULT:", result)
