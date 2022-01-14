from flask import Flask, jsonify, request

from yoloSettings import darknet_images as di
from Recommender_System_Deploy.Recommender_System import Recommender_System

import base64
import cv2
import os

#input(os.getcwd())




global img
global d
global model
global rs

app = Flask(__name__)
rs = Recommender_System()


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
        
        origin_img = cv2.imread('./yoloSettings/temp.jpg')
        height, width = origin_img.shape[:2]
        
        image, detections, class_names, class_colors = di.main(
            targetFig="./yoloSettings/temp.jpg")
        
        resized_image = cv2.resize(image,(width, height), interpolation = cv2.INTER_CUBIC)
        
        image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        base64_str = cv2.imencode('.jpg', image)[1].tostring()

        image_64 = base64.b64encode(base64_str)
        image_64 = image_64.decode('utf-8')
        
        
        res = {"image": image_64, "detections": detections,
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
            "rattingStrs": request.args.get('rattingStrs')
        }
        try:
            params['sep'] = request.args.get('sep')
        except:
            params['sep'] = ":"

        res = rs.run(**params)
        return jsonify(res)
    else:
        return jsonify('recomm connect success')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22014, debug=False)
