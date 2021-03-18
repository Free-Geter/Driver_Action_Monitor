from aip import AipBodyAnalysis

""" 你的 APPID AK SK """
APP_ID = '23824451'
API_KEY = 'YlA81wKMkpuz9iOzorx41OBs'
SECRET_KEY = '7MK9coeAt8VgemQu9oqRqGulF8QRNQ6k'

client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)


"""图片资源读取"""
def get_file_content(Path):
    with open(Path, 'rb') as fp:
        image = fp.read()
        fp.close()
    return image

"""默认识别左舵车，所有属性"""
def get_Driver_status01(file_path):
    image = get_file_content(file_path)
    result = client.driverBehavior(image);
    return result

"""识别指定行为类别，英文逗号分隔，默认所有属性都识别"""
def get_Driver_status12(file_path,attributes):
    image = get_file_content(file_path)
    options = {}
    options["type"] = attributes
    result = client.driverBehavior(image=image,options=options);
    return result

"""调整识别车辆是左舵车还是右舵车：
默认值"1"，表示左舵车（普遍适用于中国大陆地区，若图像中检测到多个大小相当的人体，默认取画面中右侧最大的人体作为驾驶员）；
"0"表示右舵车（适用于香港等地区，若图像中检测到多个大小相当的人体，则取画面中左侧最大的人体作为驾驶员）；
其他输入值视为非法输入，直接使用默认值"""
def get_Driver_status13(file_path,wheel_location):
    image = get_file_content(file_path)
    options = {}
    options["wheel_location"] = wheel_location
    result = client.driverBehavior(image=image,options=options);
    return result

"""同时指定车辆舵型、监测指标种类"""
def get_Driver_status123(file_path,attributes,wheel_location):
    image = get_file_content(file_path)
    options = {}
    options["type"] = attributes
    options["wheel_location"] = wheel_location
    result = client.driverBehavior(image=image,options=options);
    return result


if __name__ == '__main__':
    path = 'C:/Users/DELL/Desktop/driver01.jpg'
    result = get_Driver_status01(path)
    print('t_result',type(result))
    print(result)
    person_info = result['person_info']
    print('t_person_info',type(person_info))
    print(person_info)

    person_info = person_info[0]
    print('t_person',type(person_info))
    print(person_info)

    attributes = person_info["attributes"]
    print('t_attributes',type(attributes))
    print(attributes)

    eyes_closed = attributes['eyes_closed']
    print('t_eyes',type(eyes_closed))
    print(eyes_closed)

    score = eyes_closed['score']
    print('t_score',type(score))
    print(score)

