import numpy as np, cv2, sys, queue, threading
from keras.models import load_model
from keras.preprocessing import image
import AipBodyAnalysis
import Classifier
import time

classifier = cv2.CascadeClassifier(
    "D:/software/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
sys.path.append('../../api')
model = load_model('/model/model/self_trained/Overfitting-20-1.00.hdf5')

def get_image(cap, image_queue):
    c = 0
    rate = cap.get(5)
    while 1:
        c += 1
        if c % rate == 0:
            rval, img = cap.read()
            if rval:
                rval, img = cap.read()
                img = cv2.resize(img, (720, 720))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                image_queue.put(img, True)
            else:
                cv2.destroyAllWindows()
                break

def get_result(image_queue, result_queue):
    target_count = 1
    while 1:
        frame = image_queue.get(block=True)
        print(type(frame))
        faceRects = classifier.detectMultiScale(
            frame, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects):  # 大于0则检测到人脸
            for faceRect in faceRects:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                # 框出人脸
                cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
            result_queue.put(frame,True)

        # frame = image_queue.get(block=True)
        # person_info = AipBodyAnalysis.get_Driver_status01(Classifier.frame2base64(frame))
        # classed, warning = Classifier.classifier(person_info)
        # y = person_info['location']['top']
        # x = person_info['location']['left']
        # w = person_info['location']['width']
        # h = person_info['location']['height']
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # result = Classifier.change_cv2_draw(frame, warning, (x, y), 20, (0, 255, 0))
        # cv2.imwrite('C:/Users/DELL/Desktop/Slices' + '/slice' + str(target_count) + '.jpg', frame)
        # target_count += 1
        # while 1:
        #     try:
        #         result_queue.put(result.copy(), False)
        #         result[0] = image_queue.get(False)
        #     except:
        #         break


def main():
    image_queue = queue.Queue(5)
    cap = cv2.VideoCapture('MV.mp4')
    video_thread = threading.Thread(target=get_image, args=(cap, image_queue))
    video_thread.start()
    result_queue = queue.Queue(5)
    hs_thread = threading.Thread(target=get_result, args=(image_queue, result_queue))
    hs_thread.start()

    while (1):
        # rval, raw = cap.read()
        img = result_queue.get(True)
        # cv2.imshow('raw',raw)
        cv2.imshow('result', img)
        cv2.waitKey(30)

if __name__ == '__main__':
    main()