git clone https://github.com/AlexeyAB/darknet.git
cd darknet
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/LIBSO=0/LIBSO=1/' Makefile
make
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights