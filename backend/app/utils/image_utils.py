import base64
from io import BytesIO
from PIL import Image


def pil_to_base64(image: Image.Image, format: str = "PNG") -> str:
    buffer = BytesIO()
    image.save(buffer, format=format)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{encoded}"


def bytes_to_base64(image_bytes: bytes, format: str = "png") -> str:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/{format.lower()};base64,{encoded}"