import threading
import AipBodyAnalysis
from Classifier import *




class Action_Detect_Thread(threading.Thread):
    def __init__(self, in_queue, out_queue, fontsize, fontcolor,outputFile):
        # 注意：一定要显式的调用父类的初始化函数。
        super(Action_Detect_Thread, self).__init__()
        self.ok = True
        self.condition = False
        self.out_queue = out_queue
        self.in_queue = in_queue
        self.target_count = 1
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.outputFile = outputFile

    def run(self):
        while self.ok == True:
            if self.condition == True:
                if not self.in_queue.empty():
                    self.imageData = self.in_queue.get()
                    if self.imageData == 'terminal':
                        self.terminal()
                    elif self.imageData == 'in_end':
                        self.condition = False
                        self.out_queue.put('out_end')
                        print('out_end' * 10)
                    else:
                        self.detect_action(self.imageData,self.fontsize,self.fontcolor,self.outputFile)
                else:
                    self.end()

    def get_imdata(self, data):
        self.in_queue.put(data)
        self.condition = True

    def terminal(self):
        self.ok = False
        print('terminal.......')

    def end(self):
        self.condition = False

    def detect_action(self, frame, fontsize, fontcolor, outputFile):
        person_info = AipBodyAnalysis.get_Driver_status01(frame2base64(frame))
        classed, warning = classifier(person_info)

        y = person_info['location']['top']
        x = person_info['location']['left']
        w = person_info['location']['width']
        h = person_info['location']['height']
        cv2.rectangle(frame, (x, y), (x + w, y + h), fontcolor, 2)

        # 识别结果上添加警告文字
        frame = change_cv2_draw(frame, warning, (x, y), fontsize, fontcolor)

        # 输出标注后的图片
        cv2.imwrite(outputFile + '/slice_' + str(self.target_count) + '.jpg', frame)
        self.target_count += 1
        # 展示标注结果
        if self.ok:
            print(self.target_count)
            cv2.imshow('result', frame)


if __name__ == '__main__':
    for i in range(10):
        Action_Detect_Thread("thread-" + str(i)).start()
