import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image

# ✅ ABSOLUTE IMPORT (VERY IMPORTANT)
from App.moderation_engine import ModerationEngine


# ----------------------------
# App initialization
# ----------------------------
app = FastAPI(
    title="Multi-Modal NSFW Moderation API",
    description="Lightweight image, text, and video moderation system",
    version="2.1.0"
)

# Central moderation engine
engine = ModerationEngine()

# Temporary upload directory
BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "tmp_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ----------------------------
# Health check
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Multi-Modal NSFW Moderation API"
    }


# ----------------------------
# IMAGE MODERATION
# ----------------------------
@app.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        image = Image.open(file.file).convert("RGB")
        image.save(file_path)

        result = engine.moderate_image(file_path)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ----------------------------
# TEXT MODERATION
# ----------------------------
class TextRequest(BaseModel):
    text: str


@app.post("/classify-text")
async def classify_text(payload: TextRequest):
    text = payload.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    return engine.moderate_text(text)


# ----------------------------
# VIDEO MODERATION
# ----------------------------
@app.post("/classify-video")
async def classify_video(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files allowed")

    filename = f"{uuid.uuid4().hex}.mp4"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = engine.moderate_video(file_path)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
