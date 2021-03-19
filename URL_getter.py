# encoding:utf-8

import requests
import base64

'''
驾驶行为分析
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"
# 二进制方式打开图片文件
f = open('C:/Users/DELL/Desktop/driver01.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '24.d417ad1cc0176d5d192520f1989a0d4d.2592000.1618661969.282335-23824451'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())