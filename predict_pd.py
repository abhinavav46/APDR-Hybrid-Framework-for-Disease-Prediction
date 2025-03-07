#variables

num_classes =2
batch_size = 45
epochs = 20
#------------------------------

import os, cv2
from keras.models import Sequential
import numpy as np
from tensorflow.keras.models import load_model

def read_dataset1(path):
    data_list = []
    file_path = os.path.join(path)
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
    data_list.append(res)
    return (np.asarray(data_list, dtype=np.float32))


# ------------------------------
# construct CNN structure

model = Sequential()


def predictcnn_pd(fn):
    dataset=read_dataset1(fn)
    dataset=dataset / 255
    (mnist_row, mnist_col, mnist_color) = 48, 48, 1
    dataset = dataset.reshape(dataset.shape[0], mnist_row, mnist_col, mnist_color)
    mo = load_model(r"D:\softwares\Project\diabetic\model_pd.h5")
    yhat_classes = mo.predict_classes(dataset, verbose=0)
    # predict_x = mo.predict_classes(dataset, verbose=0)
    # print(predict_x)
    # maxv=max(predict_x[0])
    # print(maxv)
    # yhat_classes = np.argmax(predict_x, axis=1)
    print(yhat_classes)
    return yhat_classes

#
# label_list=["No", "Yes"]
# pred=predictcnn_pd(r"D:\softwares\Project\diabetic\myapp\static\PD_DATASET\YES\0031.png")
# print("Folder index : ", pred)
# idx=pred[0]
# print("Prediction : ", label_list[idx])