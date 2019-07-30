# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import cv2
import os

#读取单个csv中的坐标信息
def load_csv(file):
    data = pd.read_csv(file)
    img = np.zeros((8000,11400,3),np.uint8)
    for i in range(len(data['d'])):
        x = []
        y = []
        data_i = re.findall('\d+.\d',data['d'][i])  #读取第i行数据


        for k in range(int(len(data_i)/2)):
            x.append(int(float(data_i[2*k])))
            y.append(int(float(data_i[2*k+1])))

        for j in range(len(x)-1):
            cv2.line(img,(x[j],y[j]),(x[j+1],y[j+1]),(0,0,255),15)
        cv2.line(img,(x[len(x)-1],y[len(x)-1]),(x[0],y[0]),(0,0,255),15)

    img = cv2.resize(img, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_CUBIC)
    cv2.destroyWindow("contour")
    cv2.namedWindow('contour', cv2.WINDOW_AUTOSIZE)

    cv2.imshow('contour', img)
    cv2.waitKey(1000)  # how to kill the window after 10s automaticly?


    #cv2.waitKey(1000)  # how to kill the window after 10s automaticly?
    cv2.destroyAllWindows()


#line整个data文件夹中所有csv文件的图
def draw(path):
    file = os.listdir(path)
    for s in file:
        filepath = path+'/'+s
        load_csv(filepath)


if __name__ == "__main__":
    draw("E:\PYproject\BrainConnect/allen_data/region_data")
    #load_csv("E:\PYproject\BrainConnect/allen_data/region_data/1_576991103.csv")




