from flask import Flask

import numpy as np
from PIL import Image
import time
from yolov4 import Detector
from NLP.nlp_dl_training import nlp_dl_training

global img
global d
global model

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world'


@app.route('/darknet')
def darknet():
    start = time.time()

    img = Image.open('./darknet/data/dog.jpg')
    img_arr = np.array(img.resize((d.network_width(), d.network_height())))

    detections = d.perform_detect(
        image_path_or_buf=img_arr, show_image=False, thresh=0.25, make_image_only=False)
    end = time.time()
    res = f"{end-start:.3f}\n"
    for detection in detections:
        box = detection.left_x, detection.top_y, detection.width, detection.height
        res += (f'{detection.class_name.ljust(10)} | {detection.class_confidence * 100:.1f} % | {box}\n')
    return res


@app.route('/bert')
def bert():
    params = {
        "model": model,
        "nclasses": nclasses,
        "HMM": True,
        "use_paddle": False
    }
    logits, pred, ty = ndt.nlp_Bert_Predict(**params)

    return logits, pred, ty


if __name__ == '__main__':
    d = Detector(config_path='./darknet/cfg/yolov4.cfg', weights_path='./darknet/yolov4.weights',
                 meta_path='./darknet/cfg/coco.data', lib_darknet_path='./darknet/libdarknet.so', batch_size=1, gpu_id=0)

    ndt = nlp_dl_training()
    params = {
        "corpus": 'comment_zh_tw.csv',
        "HMM": True,
        "use_paddle": False,
        "epochs": 1
    }
    model, nclasses, evaluate_loss, logits, pred, ty_test = \
        ndt.nlp_Bert_Build(**params)

    app.run(host='0.0.0.0', port=5000, debug=True)
