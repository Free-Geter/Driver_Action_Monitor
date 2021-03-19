#图片检测 - OpenCV版本
import cv2
import time
filepath = "image1.jfif"
# OpenCV人脸识别分类器
classifier = cv2.CascadeClassifier(
    "D:/software/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
#记下 程序开始时间
t=time.time()
img = cv2.imread(filepath)  # 读取图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换灰色
color = (0, 255, 0)  # 定义绘制颜色
# 调用识别人脸
faceRects = classifier.detectMultiScale(
    gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
if len(faceRects):  # 大于0则检测到人脸
    for faceRect in faceRects:  # 单独框出每一张人脸
        x, y, w, h = faceRect
        # 框出人脸
        cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)

print('运行时间{}'.format(time.time()-t))
cv2.imshow("image", img)  # 显示图像
cv2.waitKey(0)  #等待按键
#cv2.destroyAllWindows()
time.sleep(5)