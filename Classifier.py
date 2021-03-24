import base64
import datetime
from queue import Queue

import test
import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from io import BytesIO
import cv2
import os

from numpy import unicode

import AipBodyAnalysis

message_Queue = Queue()
imdata_Queue = Queue()


'''
处理Person_info,返回结果字典、warning字符串
'''
def classifier(info):
    warn_dict = {
        'both_hands_leaving_wheel':'双手离开方向盘',
        'no_face_mask': '未佩戴口罩',
        'not_buckling_up': '未佩戴安全带',
        'smoke': '吸烟',
        'cellphone': '使用手机',
        'Fatigue_driving': '疲劳驾驶',
        'yawning':'打哈欠',
        'eyes_closed':'闭眼',
        'head_lowered':'低头'
    }
    classify_result = {}
    warning = "需要警告的项目：\n"
    attributes = ['both_hands_leaving_wheel','eyes_closed','no_face_mask','not_buckling_up','smoke',
                  'cellphone','yawning','head_lowered']
    if info['driver_num'] == 1:
        for a in attributes:
            if info[a]['score'] >= info[a]['threshold']:
                classify_result[a] = {'re': True, 'rate': info[a]['score']}
                warning += (warn_dict[a] + '\n')
            else:
                classify_result[a] = {'re': False, 'rate': info[a]['score']}
    elif info['driver_num'] > 1:
        print("检测到多个驾驶员！")
    elif info['driver_num'] == 0:
        print("未检测到驾驶员！")
    else:
        print("驾驶员监测错误！")
    if classify_result['eyes_closed']['re'] & classify_result['yawning']['re'] & classify_result['head_lowered']['re']:
        classify_result['Fatigue_driving'] = {'re': True, 'rate': 3}
        warning += (warn_dict['Fatigue_driving'] + '\n')
    else:
        classify_result['Fatigue_driving'] = {'re': False, 'rate': 0}


    return (classify_result,warning)

def result_disp(info):
    for k,v in info.items():
        print(k,v)

'''
图像的base64编码
'''
def frame2base64(frame):
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data  # 转码成功 返回base64编码

'''
给opencv图像添加文字
'''
def change_cv2_draw(image,strs,local,sizes,colour):
    cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    fontpath = "./simsun.ttc"  # <== 这里是宋体路径
    font = ImageFont.truetype(fontpath, 32)
    draw.text(local, strs, font=font,fill=colour)
    image = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return image



'''
创建展示窗口
'''
def windows_creater(name, width, height):
    cv2.namedWindow(name, 0);
    cv2.resizeWindow(name, int(width * (height - 80) / height), height - 80);



'''
处理并输出图像
'''
def detect(videoFile,outputFile):
    color = (0, 255, 0)  # 标注框颜色
    fontsize = 20
    fontcolor = (0, 255, 0)
    outputFile = 'C:/Users/DELL/Desktop/Slices'  # 识别结果存储地址
    if not os.path.exists(outputFile):
        os.makedirs(outputFile)
    vc = cv2.VideoCapture(videoFile)
    if vc.isOpened():
        rval, frame = vc.read()
        rate = vc.get(5)  # 帧速率
        # FrameNumber = vc.get(7)  # 视频文件的帧数
        # duration = FrameNumber / rate  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
        d_thread = test.Action_Detect_Thread(imdata_Queue, message_Queue,fontsize,fontcolor,outputFile)
        d_thread.start()
        # 视频播放计数器
        c = 1
    else:
        print('openerror!')
        rval = False
    while rval:
        rval, frame = vc.read()
        if rval:
            cv2.imshow('frame', frame)
        if c % int(rate) == 0:
            d_thread.get_imdata(frame)
        if cv2.waitKey(int(rate)) & 0xFF == ord('q'):
            break
        c += 1
    print('in_end'*10)
    d_thread.get_imdata('in_end')
    vc.release()
    cv2.destroyWindow('frame')
    while True:
        if not message_Queue.empty():
            mess = message_Queue.get()
            if mess == 'out_end':
                break
            else:
                cv2.imshow('result',mess)
        else:
            break
    cv2.destroyWindow('result')
    d_thread.terminal()



if __name__ == '__main__':
    videoFile = 'MV2.mp4'                # 待识别视频
    outputFile = 'C:/Users/DELL/Desktop/Slices'     # 识别结果存储地址
    width = 1200
    height = 800

    windows_creater('frame',800,400)
    windows_creater('result',800,400)

    detect(videoFile,outputFile)





