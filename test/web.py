import json

import cv2
import requests
import base64


def image2base64(image):
    img = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(img).decode('utf8')


def main():
    img_path = '2.png'
    with open(img_path, 'rb') as f:
        img = f.read()
    data = {
        "image": base64.b64encode(img).decode('utf8')
    }
    data = json.dumps(data)
    print('data1', len(data))
    response1 = requests.post("http://127.0.0.1:12126/ocr/english", data)
    result1 = response1.json()
    # print(json.dumps(result1, indent=4))

    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = {
        "image": image2base64(image)
    }
    data = json.dumps(data)
    print('data2', len(data))
    response = requests.post("http://127.0.0.1:12126/ocr/english", data)
    result = response.json()
    # print('result', json.dumps(result, indent=4))

    for i in range(0, len(result)):
        print(result[i]['text'], "  ==  ", result1[i]['text'])


if __name__ == '__main__':
    main()