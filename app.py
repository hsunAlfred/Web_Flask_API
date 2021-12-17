from flask import Flask

import numpy as np
from PIL import Image
import time
from yolov4 import Detector

global img
global d

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


if __name__ == '__main__':
    d = Detector(config_path='./darknet/cfg/yolov4-tiny.cfg', weights_path='./darknet/yolov4.weights',
                 meta_path='./darknet/cfg/coco.data', lib_darknet_path='./darknet/libdarknet.so', batch_size=1, gpu_id=0)
    app.run(host='0.0.0.0', port=5000)
