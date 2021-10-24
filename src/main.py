import json

import cv2
import numpy as np
import base64

import zmq

from paddle_ocr import get_english


def ocr_get_english(data):
    img = base64.b64decode(data["image"])
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    response = get_english(img)
    return {
        "code": 0,
        "message": "succeed",
        "data": response
    }


def main():
    context = zmq.Context()
    socket: zmq.Socket = context.socket(zmq.REP)
    socket.bind("tcp://*:12126")
    while True:
        data = socket.recv_json()
        if data["function"] == "/ocr/get_english":
            ret = ocr_get_english(data)
        else:
            ret = {
                "code": -1,
                "message": "not support"
            }
        socket.send_string(json.dumps(ret))


if __name__ == '__main__':
    main()
