import base64
from io import BytesIO

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
import AipBodyAnalysis




class detect_thread(QThread):
    transmit_data = pyqtSignal(dict)  # 定义信号，用于子线程与主线程中的数据交互
    def __init__(self):
        super(detect_thread, self).__init__()
        self.ok = True
        self.condition = False

    def run(self):
        while self.ok == True:
            if self.condition == True:
                self.detect_face(self.imageData)


    def get_imgdata(self,data):
        self.imageData = data
        self.condition = True

    def frame2base64(frame):
        img = Image.fromarray(frame)  # 将每一帧转为Image
        output_buffer = BytesIO()  # 创建一个BytesIO
        img.save(output_buffer, format='JPEG')  # 写入output_buffer
        byte_data = output_buffer.getvalue()  # 在内存中读取
        base64_data = base64.b64encode(byte_data)  # 转为BASE64
        return base64_data  # 转码成功 返回base64编码

    def detect_face(self,image):
        # TODO:多参数的函数选择（函数重载）
        # TODO:识别错误码
        result = AipBodyAnalysis.get_Driver_status01(self.frame2base64(image))
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
        self.transmit_data.emit(person_info)  # 如果返回结果正确，则将返回信息传递给主线程

