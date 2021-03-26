import os
import pandas as pd
import pickle
import numpy as np
import seaborn as sns
from keras_preprocessing.image import ImageDataGenerator
from sklearn.datasets import load_files
from keras.utils import np_utils
import matplotlib.pyplot as plt
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from keras.utils.vis_utils import plot_model
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from keras.preprocessing import image
from tqdm import tqdm

import seaborn as sns
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

'''
Defining the train,test and model directories
'''
DATA_DIR = "./input/state-farm-distracted-driver-detection/imgs"
TEST_DIR = os.path.join(DATA_DIR,"test")
TRAIN_DIR = os.path.join(DATA_DIR,"train")
MODEL_PATH = os.path.join(os.getcwd(),"model","self_trained")
PICKLE_DIR = os.path.join(os.getcwd(),"pickle_files")
CSV_DIR = os.path.join(os.getcwd(),"csv_files")

# if not os.path.exists(TEST_DIR):
#     print("Testing data does not exists")
# if not os.path.exists(TRAIN_DIR):
#     print("Training data does not exists")
# if not os.path.exists(MODEL_PATH):
#     print("Model path does not exists")
#     os.makedirs(MODEL_PATH)
#     print("Model path created")
# if not os.path.exists(PICKLE_DIR):
#     os.makedirs(PICKLE_DIR)
# if not os.path.exists(CSV_DIR):
#     os.makedirs(CSV_DIR)
#
# def create_csv(DATA_DIR,filename):
#     class_names = os.listdir(DATA_DIR)
#     data = list()
#     if(os.path.isdir(os.path.join(DATA_DIR,class_names[0]))):
#         for class_name in class_names:
#             file_names = os.listdir(os.path.join(DATA_DIR,class_name))
#             for file in file_names:
#                 data.append({
#                     "Filename":os.path.join(DATA_DIR,class_name,file),
#                     "ClassName":class_name
#                 })
#     else:
#         class_name = "test"
#         file_names = os.listdir(DATA_DIR)
#         for file in file_names:
#             data.append(({
#                 "FileName":os.path.join(DATA_DIR,file),
#                 "ClassName":class_name
#             }))
#     data = pd.DataFrame(data)
#     data.to_csv(os.path.join(os.getcwd(),"csv_files",filename),index=False)
#
# create_csv(TRAIN_DIR,"train.csv")
# create_csv(TEST_DIR,"test.csv")
data_train = pd.read_csv(os.path.join(os.getcwd(),"csv_files","train.csv"))
data_test = pd.read_csv(os.path.join(os.getcwd(),"csv_files","test.csv"))
data_train.info()
print('='*20)
print(data_train['ClassName'].value_counts())
print('='*20)
print(data_train.describe())

nf = data_train['ClassName'].value_counts(sort=False)
labels = data_train['ClassName'].value_counts(sort=False).index.tolist()
y = np.array(nf)
width = 1/1.5
N = len(y)
x = range(N)

fig = plt.figure(figsize=(20,15))
ay = fig.add_subplot(211)

plt.xticks(x, labels, size=15)
plt.yticks(size=15)

ay.bar(x, y, width, color="blue")

plt.title('Bar Chart',size=25)
plt.xlabel('classname',size=15)
plt.ylabel('Count',size=15)

plt.show()
print('='*20)
print(data_test.head())
print('='*20)
print(data_test.shape)
print('='*20)
print(data_train.head())
print('='*20)
print(data_train.shape)



# 转换为数字变量
labels_list = list(set(data_train['ClassName'].values.tolist()))
labels_id = {label_name:id for id,label_name in enumerate(labels_list)}
print(labels_id)
data_train['ClassName'].replace(labels_id,inplace=True)
with open(os.path.join(os.getcwd(),"pickle_files","labels_list.pkl"),"wb") as handle:
    pickle.dump(labels_id,handle)
labels = to_categorical(data_train['ClassName'])
# 一个22424行，10列的矩阵，每一行只有一个1，表示它属于10个类中的哪一个类
print(labels.shape)


# 划分数据集
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(data_train.iloc[:,0],labels,test_size = 0.2,random_state=42)

def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(64, 64))
    # convert PIL.Image.Image type to 3D tensor with shape (64, 64, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 64,64, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)

def paths_to_tensor(img_paths):
    list_of_tensors = [path_to_tensor(img_path) for img_path in tqdm(img_paths)]
    return np.vstack(list_of_tensors)

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# pre-process the data for Keras
train_tensors = paths_to_tensor(xtrain).astype('float32')/255 - 0.5
valid_tensors = paths_to_tensor(xtest).astype('float32')/255 - 0.5



#########################################################################
# model design
#########################################################################
model = Sequential()

model.add(Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(64,64,3), kernel_initializer='glorot_normal'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=128, kernel_size=2, padding='same', activation='relu', kernel_initializer='glorot_normal'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=256, kernel_size=2, padding='same', activation='relu', kernel_initializer='glorot_normal'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=512, kernel_size=2, padding='same', activation='relu', kernel_initializer='glorot_normal'))
model.add(MaxPooling2D(pool_size=2))
# 神经元随机失活，防止神经网络的预测结果过于依赖某些神经元的运算结果
model.add(Dropout(0.5))
model.add(Flatten())
# 使用线性函数拟合数据（图片的特征）的变化
model.add(Dense(500, activation='relu', kernel_initializer='glorot_normal'))
model.add(Dropout(0.5))
# 分类，使用softmax，十个输出的值的和为1
model.add(Dense(10, activation='softmax', kernel_initializer='glorot_normal'))

model.summary()

plot_model(model,to_file=os.path.join(MODEL_PATH,"model_distracted_driver.png"),show_shapes=True,show_layer_names=True)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
filepath = os.path.join(MODEL_PATH,"distracted-{epoch:02d}-{val_accuracy:.2f}.hdf5")
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max',period=1)
callbacks_list = [checkpoint]

shift_w = 0.3     # 位移强度
shift_h = 0.2
shear_range = 1.25   # 推移错切的强度
rotation_range = 25     # 旋转角度
datagen = ImageDataGenerator(width_shift_range=shift_w, height_shift_range=shift_h,
                             horizontal_flip=True,)
                             # fill_mode='constant'shear_range=shear_range,
#                              rotation_range=rotation_range,)
datagen.fit(train_tensors)
model_history = model.fit(datagen.flow(train_tensors,ytrain,batch_size=40),
                        steps_per_epoch=len(train_tensors) / 40,
                        epochs = 25,
                        callbacks=callbacks_list,
                        shuffle=True,
                        validation_data = (valid_tensors, ytest))
# model_history = model.fit(train_tensors,ytrain,validation_data = (valid_tensors, ytest),epochs=25, batch_size=40, shuffle=True,callbacks=callbacks_list)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
ax1.plot(model_history.history['loss'], color='b', label="Training loss")
ax1.plot(model_history.history['val_loss'], color='r', label="validation loss")
ax1.set_xticks(np.arange(1, 25, 1))
ax1.set_yticks(np.arange(0, 1, 0.1))

ax2.plot(model_history.history['accuracy'], color='b', label="Training accuracy")
ax2.plot(model_history.history['val_accuracy'], color='r',label="Validation accuracy")
ax2.set_xticks(np.arange(1, 25, 1))

legend = plt.legend(loc='best', shadow=True)
plt.tight_layout()
plt.show()



###############################################################
# model analysis
###############################################################
def print_confusion_matrix(confusion_matrix, class_names, figsize = (10,7), fontsize=14):
    df_cm = pd.DataFrame(
        confusion_matrix, index=class_names, columns=class_names,
    )
    fig = plt.figure(figsize=figsize)
    try:
        heatmap = sns.heatmap(df_cm, annot=True, fmt="d")
    except ValueError:
        raise ValueError("Confusion matrix values must be integers.")
    heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=fontsize)
    heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=45, ha='right', fontsize=fontsize)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    fig.savefig(os.path.join(MODEL_PATH,"confusion_matrix.png"))
    return fig


def print_heatmap(n_labels, n_predictions, class_names):
    labels = n_labels  # sess.run(tf.argmax(n_labels, 1))
    predictions = n_predictions  # sess.run(tf.argmax(n_predictions, 1))

    #     confusion_matrix = sess.run(tf.contrib.metrics.confusion_matrix(labels, predictions))
    matrix = confusion_matrix(labels.argmax(axis=1), predictions.argmax(axis=1))
    row_sum = np.sum(matrix, axis=1)
    w, h = matrix.shape

    c_m = np.zeros((w, h))

    for i in range(h):
        c_m[i] = matrix[i] * 100 / row_sum[i]

    c = c_m.astype(dtype=np.uint8)

    heatmap = print_confusion_matrix(c, class_names, figsize=(18, 10), fontsize=20)

class_names = list()
for name,idx in labels_id.items():
    class_names.append(name)
# print(class_names)
ypred = model.predict(valid_tensors)
print_heatmap(ytest,ypred,class_names)



#####################################################################
#Precision Recall F1 Score
#####################################################################
ypred_class = np.argmax(ypred,axis=1)
# print(ypred_class[:10])
ytest = np.argmax(ytest,axis=1)

accuracy = accuracy_score(ytest,ypred_class)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(ytest, ypred_class,average='weighted')
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(ytest,ypred_class,average='weighted')
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(ytest,ypred_class,average='weighted')
print('F1 score: %f' % f1)
