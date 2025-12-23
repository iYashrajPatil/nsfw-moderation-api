from fastapi import FastAPI, UploadFile, File
import os
import uuid
from App.classifier import NSFWDetector

app = FastAPI(title="NSFW Moderation API")

# Create temp upload directory
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

detector = NSFWDetector()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1]
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = detector.classify(temp_path)
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
