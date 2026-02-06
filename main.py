from fastapi import FastAPI, UploadFile
import shutil
import json
import re

from app.analysis import analyze_oranges
from app.gemini import classify_oranges_full

app = FastAPI()


@app.post("/analyze")
async def analyze(file: UploadFile):

    with open("input.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Roboflow detection
    analysis = analyze_oranges("input.jpg")
    boxes = analysis["boxes"]

    # Gemini classification
    raw = classify_oranges_full("input.jpg", boxes)

    match = re.search(r"\[.*\]", raw, re.S)

    if not match:
        return {
            "error": "Gemini failed to return JSON",
            "raw": raw
        }

    health = json.loads(match.group())

    """calculation of spoilage percentage : this is estimationa and the n(fruits detected by gemini) is considered as total fruits seen by gemini """

    total_seen = len(health)

    healthy = sum(
        1 for o in health if o["status"] == "healthy_orange"
    )

    spoiled = total_seen - healthy

    spoilage_percentage = round((spoiled / total_seen) * 100, 2) if total_seen else 0

    return {
        "total_oranges_detected": analysis["total_oranges"],
        "oranges_seen_by_gemini": total_seen,
        "average_size_px": analysis["average_size_px"],
        "spoilage_percentage": spoilage_percentage,
        "annotated_image": analysis["annotated_image"],
        "health_report": health
    }
