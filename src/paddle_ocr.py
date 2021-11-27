from paddleocr import PaddleOCR


# https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_server_v2.0_det_infer.tar
# https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar
# https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_server_v2.0_rec_infer.tar
ocr_ch_fast = None


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


def ocr_get_text(img):
    global ocr_ch_fast

    if ocr_ch_fast is None:
        ocr_ch_fast = PaddleOCR(
            show_log=False,
            use_angle_cls=True,
            lang='ch',
            det_model_dir="./model/ch_ppocr_server_v2.0_det_infer",
            rec_model_dir="./model/ch_PP-OCRv2_rec_infer",
            cls_model_dir="./model/ch_ppocr_mobile_v2.0_cls_infer"
        )
    # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
    # You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
    # to switch the language model in order.
    result = ocr_ch_fast.ocr(img)
    data = []
    for line in result:
        print("line: ", line)
        item = {
            "rect": get_rect(line[0]),
            "text": line[1][0],
            "score": float(line[1][1]),
        }
        data.append(item)
    return data
