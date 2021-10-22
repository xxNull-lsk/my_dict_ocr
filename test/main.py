from paddleocr import PaddleOCR


def main():
    # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
    # You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
    # to switch the language model in order.
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to download and load model into memory
    img_path = '1.png'
    result = ocr.ocr(img_path, cls=True)
    print(result)
    for line in result:
        print(line)


if __name__ == '__main__':
    main()
