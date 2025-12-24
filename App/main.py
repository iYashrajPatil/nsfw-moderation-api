import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from classifier import NSFWDetector
from PIL import Image


app = FastAPI(
    title="NSFW Moderation API",
    description="Image moderation using NudeNet",
    version="1.0.0"
)

detector = NSFWDetector()

UPLOAD_DIR = "tmp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "NSFW Moderation API"
    }


@app.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        image = Image.open(file.file).convert("RGB")
        image.save(file_path)

        result = detector.classify(file_path)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
