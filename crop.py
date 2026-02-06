from PIL import Image
import os


def crop_oranges(image_path, boxes, out_dir="crops"):

    os.makedirs(out_dir, exist_ok=True)

    img = Image.open(image_path)

    paths = []

    for i, b in enumerate(boxes):
        x = b["x"]
        y = b["y"]
        w = b["width"]
        h = b["height"]

        crop = img.crop((
            x - w / 2,
            y - h / 2,
            x + w / 2,
            y + h / 2
        ))

        path = f"{out_dir}/orange_{i}.jpg"
        crop.convert("RGB").save(path)
        paths.append(path)

    return paths
