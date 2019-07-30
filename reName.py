#-*- coding: utf-8 -*-
# author:yuan_lei
# datetime:2019/7/17 13:04



import os
path = "E:\pyProgram\BrainConnect/real\img"
# reNAME(path):
allFile = os.listdir(path)
allFile.sort(key = lambda x: int(x[1:]))

i = 0
for file in allFile:
    i += 1
    newname = 's'+str(i)+".png"
    os.rename(os.path.join(path,file),os.path.join(path,newname))




# reNAME("E:\PYproject\BrainConnect/allen_data/test")