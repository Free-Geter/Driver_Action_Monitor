import cv2
import os

videoFile = '/Users/apple/Downloads/MV.mp4'
outputFile = '/Users/apple/Downloads/MV_slices'
if not os.path.exists(outputFile):
    os.makedirs(outputFile)

vc = cv2.VideoCapture(videoFile)
c = 1
if vc.isOpened():
    rval, frame = vc.read()
else:
    print('openerror!')
    rval = False

timeF = 100  #视频帧计数间隔次数
while rval:
    print(1)
    rval, frame = vc.read()
    if c % timeF == 0:
        print(2)
        cv2.imwrite(outputFile + '/slice' + str(int(c / timeF)) + '.jpg', frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break
    c += 1
vc.release()


