from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from classifier import NSFWDetector

app = FastAPI(title="NSFW Image Moderation API")

detector = NSFWDetector()

@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = detector.classify(tmp_path)
    os.remove(tmp_path)

    return result
