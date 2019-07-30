#-*- coding: utf-8 -*-
# author:yuan_lei
# datetime:2019/7/17 19:12

import cv2
import os

def compression(path):
    for file in os.listdir(path):
        img = cv2.imread(path+'/'+file,0)
        #res = cv2.resize(img,(512,512))
        cv2.imwrite(path+'/'+file,img)


compression("E:\pyProgram\BrainConnect/real\img")