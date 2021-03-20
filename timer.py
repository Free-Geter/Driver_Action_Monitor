import datetime

from Classifier import *
    # info_getter,frame2base64,classifier,result_disp,change_cv2_draw


if __name__ == '__main__':
    videoFile = 'MV.mp4'                # 待识别视频
    outputFile = 'C:/Users/DELL/Desktop/Slices'     # 识别结果存储地址
    timeF = 30                          # 视频帧计数间隔次数
    color = (0, 255, 0)                 # 标注框颜色
    fontsize = 20
    fontcolor = (0, 255, 0)
    if not os.path.exists(outputFile):
        os.makedirs(outputFile)
    vc = cv2.VideoCapture(videoFile)
    c = 1
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        print('openerror!')
        rval = False


    while rval:
        starttime = datetime.datetime.now()
        # long running
        # do something other
        rval, frame = vc.read()
        if c % timeF == 0:
            print('='*60)
            person_info = info_getter(frame2base64(frame))
            classed,warning = classifier(person_info)
            result_disp(classed)
            y = person_info['location']['top']
            x = person_info['location']['left']
            w = person_info['location']['width']
            h = person_info['location']['height']
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # 识别结果上添加警告文字
            frame = change_cv2_draw(frame,warning,(x,y),fontsize,fontcolor)

            # 输出标注后的图片
            cv2.imwrite(outputFile + '/slice' + str(int(c / timeF)) + '.jpg', frame)

            endtime = datetime.datetime.now()
            sec = (endtime - starttime).seconds
            print('time{0}: {1}'.format(c, sec))

            # 展示标注结果
            # width = 1200
            # height = 800
            # cv2.namedWindow("frame", 0);
            # cv2.resizeWindow('frame',int(width * (height - 80) / height), height - 80);
            # cv2.imshow('frame', frame)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break
        c += 1
    vc.release()