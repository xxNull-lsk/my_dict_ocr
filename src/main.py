import datetime
import json
import threading

import cv2
import numpy as np
import base64

import zmq

version = "0.0.2"


def get_text(data):
    from paddle_ocr import ocr_get_text
    img = base64.b64decode(data["image"])
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    response = ocr_get_text(img)
    return {
        "code": 0,
        "message": "succeed",
        "data": response
    }


def do_first_run():
    context = zmq.Context()
    socket: zmq.Socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:12126")
    socket.setsockopt(zmq.RCVTIMEO, 10000)
    socket.setsockopt(zmq.SNDTIMEO, 5000)
    mat = cv2.imread("./first.png")
    img = cv2.imencode('.jpg', mat)[1]
    data = {
        "function": "/ocr/get_text",
        "image": base64.b64encode(img).decode('utf8')
    }

    begin = datetime.datetime.now()
    socket.send_string(json.dumps(data))
    response = socket.recv_string()
    response = json.loads(response)
    used = datetime.datetime.now() - begin
    print(json.dumps(response, indent=4), "\nused: ", used.total_seconds())


def main():
    context = zmq.Context()
    socket: zmq.Socket = context.socket(zmq.REP)
    socket.bind("tcp://*:12126")

    t = threading.Thread(target=do_first_run)
    t.start()

    while True:
        data = socket.recv_json()
        begin = datetime.datetime.now()
        print("{} recv: {} {}".format(begin, data["function"], len(json.dumps(data))))
        if data["function"] == "/ocr/get_english":
            ret = get_text(data)
        elif data["function"] == "/ocr/get_text":
            ret = get_text(data)
        elif data["function"] == "/version":
            ret = {
                "code": 0,
                "message": "succeed",
                "version": version
            }
        elif data["function"] == "/tick":
            ret = {
                "code": 0,
                "message": "succeed"
            }
        else:
            ret = {
                "code": -1,
                "message": "not support"
            }
        now = datetime.datetime.now()
        used = now - begin
        print("{} used: {}".format(now, used.total_seconds()))
        socket.send_string(json.dumps(ret))


if __name__ == '__main__':
    main()
