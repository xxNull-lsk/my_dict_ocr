import base64
import datetime
import json

import zmq
import cv2


context = zmq.Context()
socket: zmq.Socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:12126")
socket.setsockopt(zmq.RCVTIMEO, 5000)
socket.setsockopt(zmq.SNDTIMEO, 500)

mat = cv2.imread("./2.png")

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
