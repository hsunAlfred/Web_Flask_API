from yoloSettings import darknet_images as di
import base64

with open('./yoloSettings/test1.jpg', 'rb') as f:
    img_64 = base64.b64encode(f.read())

# with open('./yoloSettings/temp.jpg', 'wb') as f:
#     img_data = base64.b64decode(
#         str(img_64).replace('data:image/jpg;base64,', ''))
#     f.write(img_data)
    # f.write(f"data:image/jpg;base64,{str(img_64)[2:-1]}")

# res = di.main(targetFig="./yoloSettings/temp.jpg")

res = di.main(targetFig=f"data:image/jpeg;base64"+img_64)
print(res)
