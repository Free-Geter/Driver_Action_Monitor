import base64

import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from io import BytesIO
import cv2
import os

from numpy import unicode

import AipBodyAnalysis



def info_getter(path):
    result = AipBodyAnalysis.get_Driver_status01(path)
    print('t_result', type(result))
    print(result)

    person_info = {
        'person_num': result['person_num'],
        'driver_num': result['driver_num'],
        'attributes': result['person_info'][0]["attributes"],
        'location': result['person_info'][0]['location'],
        'both_hands_leaving_wheel': result['person_info'][0]["attributes"]['both_hands_leaving_wheel'],
        'eyes_closed': result['person_info'][0]["attributes"]['eyes_closed'],
        'no_face_mask': result['person_info'][0]["attributes"]['no_face_mask'],
        'not_buckling_up': result['person_info'][0]["attributes"]['not_buckling_up'],
        'smoke': result['person_info'][0]["attributes"]['smoke'],
        'cellphone': result['person_info'][0]["attributes"]['cellphone'],
        'yawning': result['person_info'][0]["attributes"]['not_facing_front'],
        'head_lowered': result['person_info'][0]["attributes"]['head_lowered']
    }

    # for k, v in person_info.items():
    #     print(type(v))
    #     print(k, v)

    return person_info


def classifier(info):
    warn_dict = {
        'both_hands_leaving_wheel':'双手离开键盘',
        'no_face_mask': '未佩戴口罩',
        'not_buckling_up': '未佩戴安全带',
        'smoke': '吸烟',
        'cellphone': '使用手机',
        'Fatigue_driving': '疲劳驾驶'
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
        print(type(v))
        print(k,v)

def frame2base64(frame):
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data  # 转码成功 返回base64编码


def change_cv2_draw(image,strs,local,sizes,colour):
    cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    fontpath = "./simsun.ttc"  # <== 这里是宋体路径
    font = ImageFont.truetype(fontpath, 32)
    draw.text(local, strs, font=font,fill=colour)
    image = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return image


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






