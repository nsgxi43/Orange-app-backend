import os
from dotenv import load_dotenv
from roboflow import Roboflow

load_dotenv()

rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
project = rf.workspace().project("fruit2-ofw6x")
model = project.version(1).model


def analyze_oranges(image_path):

    result = model.predict(image_path, confidence=40, overlap=30)

    boxes = result.json()["predictions"]

    result.save("annotated.jpg")

    sizes = []

    for b in boxes:
        w = b["width"]
        h = b["height"]
        sizes.append((w * h) ** 0.5)

    avg_size = sum(sizes) / len(sizes) if sizes else 0

    return {
        "total_oranges": len(boxes),
        "average_size_px": round(avg_size, 2),
        "boxes": boxes,
        "annotated_image": "annotated.jpg"
    }
