import base64

from aip import AipBodyAnalysis

""" 你的 APPID AK SK """
APP_ID = '23824451'
API_KEY = 'YlA81wKMkpuz9iOzorx41OBs'
SECRET_KEY = '7MK9coeAt8VgemQu9oqRqGulF8QRNQ6k'

client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
#创建客户端
"""图片资源读取"""


def get_file_content(Path):
    with open(Path, 'rb') as fp:
        image = fp.read()
        fp.close()
    return image

def get_status(image,attributes=None,wheel_location=None):
    if attributes == None & wheel_location == None:
        get_Driver_status01(image)
    elif attributes != None & wheel_location == None:
        get_Driver_status12(image,attributes)
    elif attributes == None & wheel_location != None:
        get_Driver_status13(image,wheel_location)
    else:
        get_Driver_status123(image,attributes,wheel_location)

#json格式转换
def conver_result(result):
    if 'error_code' in result.keys():
        print('error_code:', result['error_code'])
        print('error_msg:', result['error_msg'])
        return 0
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
    return person_info

"""默认识别左舵车，所有属性"""

#发送图片
def get_Driver_status01(image):
#     image = get_file_content(file_path)
    result = client.driverBehavior(image)
    return conver_result(result)


"""识别指定行为类别，英文逗号分隔，默认所有属性都识别"""


def get_Driver_status12(image, attributes):
    # image = get_file_content(file_path)
    options = {}
    options["type"] = attributes
    result = client.driverBehavior(image=image, options=options);
    return conver_result(result)


"""调整识别车辆是左舵车还是右舵车：
默认值"1"，表示左舵车（普遍适用于中国大陆地区，若图像中检测到多个大小相当的人体，默认取画面中右侧最大的人体作为驾驶员）；
"0"表示右舵车（适用于香港等地区，若图像中检测到多个大小相当的人体，则取画面中左侧最大的人体作为驾驶员）；
其他输入值视为非法输入，直接使用默认值"""


def get_Driver_status13(image, wheel_location):
    # image = get_file_content(file_path)
    options = {}
    options["wheel_location"] = wheel_location
    result = client.driverBehavior(image=image, options=options);
    return conver_result(result)


"""同时指定车辆舵型、监测指标种类"""


def get_Driver_status123(image, attributes, wheel_location):
    # image = get_file_content(file_path)
    options = {}
    options["type"] = attributes
    options["wheel_location"] = wheel_location
    result = client.driverBehavior(image=image, options=options)
    return conver_result(result)


if __name__ == '__main__':
    path = 'test.png'
    path = base64.b64encode(get_file_content(path)).decode()
    result = get_Driver_status01(path)
    print('t_result', type(result))
    print(result)

    person_info = {
        'person_num': result['person_num'],
        'driver_num': result['driver_num'],
        'attributes': result['person_info'][0]["attributes"],
        'location': result['person_info'][0]['location'],
        'both_hands_leaving_wheel' : result['person_info'][0]["attributes"]['both_hands_leaving_wheel'],
        'eyes_closed' : result['person_info'][0]["attributes"]['eyes_closed'],
        'no_face_mask': result['person_info'][0]["attributes"]['no_face_mask'],
        'not_buckling_up': result['person_info'][0]["attributes"]['not_buckling_up'],
        'smoke': result['person_info'][0]["attributes"]['smoke'],
        'cellphone': result['person_info'][0]["attributes"]['cellphone'],
        'yawning': result['person_info'][0]["attributes"]['not_facing_front'],
        'head_lowered': result['person_info'][0]["attributes"]['head_lowered']
    }

    # for k,v in person_info.items():
    #     print(type(v))
    #     print(k,v)