# **一. 主要功能**

1. 调研医学图像三维重建算法，对allen图谱实现三维重建，且可旋转查看。

2. 导入乳头体区域图谱切片的坐标文件（xml格式），得到乳头体区域的三维重建结果。

3. 可用任意平面对重建的三维图像切割，得到任意角度的切片。

   ------

# **二. 实现效果**

## 1. allen图谱的三维重建

经过对三维重现算法的调研，最终采用 *MC (Matching Cubes)* 算法，MC算法能够很好的对CT等医学图像进行三维复现。

下图展示的是对allen图谱的重建结果，一共使用了132张切片，可拖动鼠标实现图像旋转，实现任意角度查看图像。

![image](https://github.com/lovvtin/MC_3D_cutter/blob/master/456.PNG)



## **2.乳头体区域图谱的三维重建**

下图展示了乳头体区域图谱的重建结果，一共调用了20张切片，

![image](https://github.com/lovvtin/MC_3D_cutter/blob/master/3D.PNG)

## **3. 获取allen图谱任意角度切片**

输入平面上一点的坐标以及平面法向量，得到该平面截取的图像。

如下图所示，图中黑色的线表示截取三维图像的平面

![image](https://github.com/lovvtin/MC_3D_cutter/blob/master/4654.PNG)
下图是截取到的切片：

![iamge](https://github.com/lovvtin/MC_3D_cutter/blob/master/7987.PNG)

## 4. 获取乳头体区域谱图任意角度切片

同理，输入平面上一点的坐标以及平面法向量，得到该平面截取的图像。

如下图所示，图中黑色的线表示截取三维图像的平面

![image](https://github.com/lovvtin/MC_3D_cutter/blob/master/1.PNG)

下图是截取到的乳头体区域切片：

![image](https://github.com/lovvtin/MC_3D_cutter/blob/master/123.PNG)

