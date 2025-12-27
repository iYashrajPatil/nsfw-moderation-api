from text_moderator.text_moderator import TextModerator

moderator = TextModerator()

samples = [
    "hello how are you",
    "this is a normal comment",
    "she is nude in the picture",
    "fuck this shit",
    "send me porn videos",
    "you are such a bitch",
    "I love beaches and summer"
]

for text in samples:
    result = moderator.classify(text)
    print(f"TEXT: {text}")
    print("RESULT:", result)
    print("-" * 50)
