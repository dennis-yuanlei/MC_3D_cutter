#-*- coding: utf-8 -*-
# author:yuanlei
# datetime:2019/7/11 9:52


import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt

#读取单个csv中的坐标信息
def load_csv_draw(file):
    data = pd.read_csv(file)
    plt.figure()
    for i in range(len(data['d'])):
        data_i = re.findall('\d+.\d',data['d'][i])  #读取第i行数据
        x = []
        y = []

        for k in range(int(len(data_i)/2)):
            x.append(int(float(data_i[2*k])))
            y.append(int(float(data_i[2*k+1])))

        plt.plot(x,y,color='c')
    plt.show()

def load_all(path):
    file = os.listdir(path)
    for f in file:
        filePath = path + '/' + f
        #load_csv_draw(filePath)
        print (f[0:3])


if __name__ == "__main__":
    #load_csv_draw("E:\PYproject\BrainConnect/allen_data/region_data/1_576991103.csv")
    load_all("E:\PYproject\BrainConnect/allen_data/region_data")