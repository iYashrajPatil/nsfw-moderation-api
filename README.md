# NSFW Moderation API

A Python-based image moderation system using **NudeNet**.

## Features
- Detects explicit and suggestive content
- Classifies images as SAFE / NSFW / REVIEW
- Lazy model loading (efficient)
- Clean FastAPI backend

## Tech Stack
- Python
- FastAPI
- NudeNet
- ONNX Runtime

## Usage
Upload an image to `/classify-image` endpoint to get moderation result.

## Note
Model files are intentionally not committed to the repository.
