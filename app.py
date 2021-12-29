from flask import Flask, jsonify, request

from yoloSettings import darknet_images as di
from Recommender_System_Deploy.Recommender_System import Recommender_System

import base64

global img
global d
global model
global rs

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world'


@app.route('/yolo', methods=['POST', 'GET'])
def yolo():
    if request.method == 'POST':
        img_64 = request.args.get('img').replace(
            ' ', '+').replace("data:image/jpeg;base64,", '')

        with open('./yoloSettings/temp.jpg', 'wb') as f:
            img_data = base64.b64decode(img_64)
            f.write(img_data)

        image, detections, class_names, class_colors = di.main(
            targetFig="./yoloSettings/temp.jpg")
        res = {"image": str(image), "detections": detections,
               "class_names": class_names, "class_colors": class_colors}
        #res = di.main(targetFig=img_64)

        return jsonify(res)
    else:
        return jsonify('yolo connect success')


@app.route('/recomm', methods=['POST', 'GET'])
def recomm():
    if request.method == 'POST':
        params = {
            "thisBendom": request.args.get('thisBendom'),
            "ratting": request.args.get('ratting')
        }
        res = rs.run(**params)
        return jsonify(res)
    else:
        return jsonify('recomm connect success')


if __name__ == '__main__':
    rs = Recommender_System()

    app.run(host='0.0.0.0', port=5000, debug=True)
