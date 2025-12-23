# NSFW Image Moderation API

A backend service for **image-based NSFW moderation** built using **FastAPI** and **NudeNet**, designed for social media and content platforms.

The API classifies uploaded images into:
- SAFE
- REVIEW
- NSFW

This system focuses on **balanced moderation**, avoiding over-penalization of normal clothing while still flagging explicit content.

---

## Features

- Image-based NSFW detection
- REST API using FastAPI
- Gender-neutral moderation logic
- Handles real-world clothing scenarios (traditional, gym wear, casual)
- Ready for frontend integration
- Deployable on cloud platforms (Render)

---

## Tech Stack

- Python
- FastAPI
- NudeNet (ONNX / YOLO-based)
- Uvicorn

---

## Project Structure

```text
NSFW-moderation/
├── App/
│   ├── main.py
│   ├── classifier.py
│   └── requirements.txt
├── render.yaml
└── README.md

## API Endpoint

### POST /moderate

Uploads an image and returns a moderation verdict.




