from fastapi import FastAPI, UploadFile, File
import shutil
import uuid
import os

from App.classifier import NSFWDetector

app = FastAPI(title="NSFW Moderation API")

# ✅ Safe: constructor does NOT load model
detector = NSFWDetector()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    # Save uploaded image to temp location
    suffix = os.path.splitext(file.filename)[-1]
    temp_path = f"/tmp/{uuid.uuid4()}{suffix}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = detector.classify(temp_path)
        return result
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
