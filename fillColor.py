#-*- coding: utf-8 -*-
# author:yuan_lei
# datetime:2019/7/17 17:25

import os
import cv2

def fillColor(image,window):
    imgfile = image
    img = cv2.imread(imgfile)
    h, w, _ = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find Contour
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)



    for i in range(len(contours)-1):
        cv2.drawContours(img, contours, i+1, (0, 134, 139), thickness= -1)
        cv2.drawContours(img, contours, i+1, (0, 0, 255), thickness=2)

    cv2.imwrite(image, img)
    cv2.imshow(window, img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

def loadImg(path):
    fileAll = os.listdir(path)
    fileAll.sort(key=lambda x:int(x[1:-4]))
    for pic in fileAll:
        fillColor(path+'/'+pic,pic)

loadImg("E:\pyProgram\BrainConnect/real\img")
