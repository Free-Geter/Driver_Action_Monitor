import cv2
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
import numpy as np
import Classifier

model = load_model('F:/workspace/Driver_Action_Monitor/model/model/self_trained/distracted-20-1.00.hdf5')
def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(64, 64))
    # convert PIL.Image.Image type to 3D tensor with shape (64, 64, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 64,64, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)

def video_to_tensor(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    width = 1200
    height = 800
    cv2.namedWindow("result", 0);
    cv2.resizeWindow('result', int(width * (height - 80) / height), height - 80);
    while True:
        ret, frame = cap.read()
        if ret == True:
            img = Image.fromarray(frame)  # 完成np.array向PIL.Image格式的转换
            # print('img type',type(img))
            img = img.resize((64, 64))
            x = image.img_to_array(img)
            tensors = np.expand_dims(x, axis=0)
            # convert 3D tensor to 4D tensor with shape (1, 64,64, 3) and return 4D tensor
            result = model.predict(tensors)[0]
            action_dict = {
                'texting - left': result[0],
                'talking on the phone - left': result[1],
                'texting - right': result[2],
                'talking to passenger': result[3],
                'hair and makeup': result[4],
                'operating the radio': result[5],
                'reaching behind': result[6],
                'drinking': result[7],
                'talking on the phone - right': result[8],
                'normal driving': result[9]
            }
            warning = max(action_dict, key=action_dict.get)
            cv2.putText(frame, warning, (100, 300), cv2.FONT_HERSHEY_SIMPLEX,
                        3, (255, 255, 255), 3, cv2.LINE_AA)
            #re_frame = Classifier.change_cv2_draw(frame, warning, (100,100), 20, (0, 255, 0))
            cv2.imshow('result',frame)
            cv2.waitKey(1)
            print('='*30)
            print(warning)
        else:
            break
            # cv2.imshow("frame", frame)  # 正常显示frame
            # cv2.waitKey(1)

def detect_test(img_path):
    # model.summary()
    tensors = path_to_tensor(img_path).astype('float32') / 255 - 0.5
    result = model.predict(tensors)[0]
    action_dict = {
        'texting - left': result[0],
        'talking on the phone - left': result[1],
        'texting - right': result[2],
        'talking to passenger': result[3],
        'hair and makeup': result[4],
        'operating the radio': result[5],
        'reaching behind': result[6],
        'drinking': result[7],
        'talking on the phone - right': result[8],
        'normal driving': result[9]
    }
    print(max(action_dict,key=action_dict.get))


if __name__ == '__main__':
    video_to_tensor('../MV.mp4')
    # detect_test('F:/workspace/Driver_Action_Monitor/model/input/state-farm-distracted-driver-detection/imgs/train/c9/img_19.jpg')


# laber_dict = {'c3': 'texting - left',
# 'c4': 'talking on the phone - left',
# 'c1': 'texting - right',
# 'c9': 'talking to passenger',
# 'c8': 'hair and makeup',
# 'c5': 'operating the radio',
# 'c7': 'reaching behind',
# 'c6': 'drinking',
# 'c2': 'talking on the phone - right',
# 'c0': 'normal driving'}

