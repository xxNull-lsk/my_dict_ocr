import cv2
from fastapi import FastAPI
import numpy as np
import base64
from pydantic import BaseModel
import uvicorn

from src.paddle_ocr import get_english

app = FastAPI()


class Ocr(BaseModel):
    image: str


@app.post("/ocr/english")
def ocr_english(req: Ocr):
    img = base64.b64decode(req.image)
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return get_english(img)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=12126, reload=True, debug=True)
