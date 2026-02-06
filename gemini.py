from dotenv import load_dotenv
load_dotenv()

from google import genai
from PIL import Image
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def classify_oranges_full(image_path, boxes):

    image = Image.open(image_path)

    prompt = f"""
You are an agriculture quality inspector.

You are given an image of oranges and bounding boxes detected by a model.

Bounding boxes (index based):

{json.dumps(boxes, indent=2)}

For EACH box index, classify strictly as:

healthy_orange
rotten_orange
fungus_orange

Return ONLY JSON array like:

[
 {{ "box": 0, "status": "healthy_orange" }},
 {{ "box": 1, "status": "healthy_orange" }}
]

No explanation.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt, image]
    )

    if response.text:
        return response.text

    parts = []
    for c in response.candidates:
        for p in c.content.parts:
            if hasattr(p, "text"):
                parts.append(p.text)

    return "\n".join(parts)
