from flask import Flask, jsonify, request

import numpy as np
from PIL import Image
import time
from yolov4 import Detector
# from NLP.nlp_dl_training import nlp_dl_training
from yoloSettings import darknet_images as di

import base64

global img
global d
global model

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world'


# @app.route('/darknet')
# def darknet():
#     start = time.time()

#     img = Image.open('./darknet/data/dog.jpg')
#     img_arr = np.array(img.resize((d.network_width(), d.network_height())))

#     detections = d.perform_detect(
#         image_path_or_buf=img_arr, show_image=False, thresh=0.25, make_image_only=False)
#     end = time.time()
#     res = f"{end-start:.3f}\n"
#     for detection in detections:
#         box = detection.left_x, detection.top_y, detection.width, detection.height
#         res += (f'{detection.class_name.ljust(10)} | {detection.class_confidence * 100:.1f} % | {box}\n')
#     return res


@app.route('/yolo', methods=['POST', 'GET'])
def yolo():
    if request.method == 'GET':
        img_64 = request.args.get('img').replace(
            ' ', '+').replace("data:image/jpeg;base64,", '')

        with open('./yoloSettings/temp.jpg', 'wb') as f:
            img_data = base64.b64decode(img_64)
            f.write(img_data)

        res = di.main(targetFig="./yoloSettings/temp.jpg")

        #res = di.main(targetFig=img_64)

        return jsonify(res[1])
    else:
        return 'connect success'


# @app.route('/bert')
# def bert():
#     params = {
#         "model": model,
#         "nclasses": nclasses,
#         "HMM": True,
#         "use_paddle": False
#     }
#     logits, pred, ty = ndt.nlp_Bert_Predict(**params)

#     #rest = {"logits":list(logits),"pred":list(pred),"ty":list(ty)}

#     return "Done"


if __name__ == '__main__':
    # d = Detector(config_path='./yoloSettings/yolov4-BukaCa.cfg', weights_path='./yoloSettings/yolov4-BukaCa_last.weights',
    #              meta_path='./yoloSettings/BukaCa.data', lib_darknet_path='./darknet/libdarknet.so', batch_size=1, gpu_id=0)

    # ndt = nlp_dl_training()
    # params = {
    #     "corpus": './NLP/comment_zh_tw.csv',
    #     "HMM": True,
    #     "use_paddle": False,
    #     "epochs": 1
    # }
    # model, nclasses, evaluate_loss, logits, pred, ty_test = \
    #     ndt.nlp_Bert_Build(**params)

    app.run(host='0.0.0.0', port=5000, debug=True)
