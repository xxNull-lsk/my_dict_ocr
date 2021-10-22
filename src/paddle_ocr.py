from paddleocr import PaddleOCR


ocr_eng = PaddleOCR(use_angle_cls=True, lang='en')


def get_rect(pos):
    x = 999999
    y = 999999
    x2 = 0
    y2 = 0
    for pt in pos:
        x = min(x, pt[0])
        y = min(y, pt[1])
        x2 = max(x2, pt[0])
        y2 = max(y2, pt[1])
    return [x, y, x2 - x + 1, y2 - y + 1]


def get_english(img):
    # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
    # You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
    # to switch the language model in order.
    result = ocr_eng.ocr(img, cls=True)
    data = []
    for line in result:
        print("line: ", line, '\n\n')
        item = {
            "rect": get_rect(line[0]),
            "text": line[1][0],
            "score": float(line[1][1]),
        }
        data.append(item)
    return data
