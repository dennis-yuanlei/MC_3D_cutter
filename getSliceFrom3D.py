#-*- coding: utf-8 -*-
# author:yuan_lei
# datetime:2019/7/18 20:24


import vtk

def main():

    colors = vtk.vtkNamedColors()
    colors.SetColor("SkinColor", [139, 69, 0, 255])
    colors.SetColor("BkgColor", [139, 131, 120, 255])

    #############################################################
    #读取PNG图像，必须是灰度图像

    reader = vtk.vtkPNGReader()
    reader.SetFileDimensionality(2)#存储在文件中的维数
    reader.SetFilePrefix("E:\pyProgram\BrainConnect/allen_data\img512/s") #指定图像文件的前缀
    #reader.SetFileNameSliceSpacing()#当读取具有常规但非连续切片的文件（例如filename.1，filename.3，filename.5）时，可以指定间距以跳过丢失的文件（默认值= 1）
    reader.SetFilePattern("%s%d.png")#配合SetFilePrefix使用，用于从FilePrefix和切片编号构建文件名的snprintf样式格式字符串
    reader.SetDataExtent( 0, 511, 0, 511, 0, 131)#设置disk数据范围，前两个为img大小，最后一个为slice数量
    reader.SetDataSpacing(1,1,4)  #设置文件中数据的间距

    ############################################################

    # An isosurface, or contour value of 500 is known to correspond to the
    # skin of the patient.
    #**************************************************************************
    skinExtractor = vtk.vtkMarchingCubes()
    skinExtractor.SetInputConnection(reader.GetOutputPort())
    skinExtractor.SetValue(0, 80)
    #**************************************************************************

    skinMapper = vtk.vtkPolyDataMapper()#vtkPolyDataMapper是一个将多边形数据（即vtkPolyData）映射到图形基元的类
    skinMapper.SetInputConnection(skinExtractor.GetOutputPort())

    # create a plane to cut,here it cuts in the XZ direction (xz normal=(1,0,0);XY =(0,0,1),YZ =(0,1,0)
    plane = vtk.vtkPlane()
    plane.SetOrigin(180, 290, 204)
    plane.SetNormal(1, 31, 10)#平面的法向量

    # create cutter
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(skinExtractor.GetOutputPort())
    cutter.Update()
    cutterMapper = vtk.vtkPolyDataMapper()
    cutterMapper.SetInputConnection(cutter.GetOutputPort())

    # create plane actor
    planeActor = vtk.vtkActor()
    planeActor.GetProperty().SetColor(0, 0, 0)
    planeActor.GetProperty().SetLineWidth(5)
    planeActor.SetMapper(cutterMapper)

    #create skin actor
    skin = vtk.vtkActor()
    skin.SetMapper(skinMapper)
    skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))

    # create renderers and add actors of plane and skin
    ren = vtk.vtkRenderer()
    ren.AddActor(planeActor)
    ren.AddActor(skin)

    #添加axes
    transform = vtk.vtkTransform()
    transform.Translate(0.0, 0.0, 0.0)
    axes = vtk.vtkAxesActor()
    #  The axes are positioned with a user transform
    axes.SetUserTransform(transform)
    ren.AddActor(axes)
    axes.SetTotalLength(70.0, 70.0, 70.0)#设置坐标轴长短
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(colors.GetColor3d("Red"))#设置坐标轴颜色
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(colors.GetColor3d("Yellow"))
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(colors.GetColor3d("White"))
    ###############################################

    aCamera = vtk.vtkCamera()
    aCamera.SetViewUp(1, 0, 0)#设置相机查看方向
    aCamera.SetPosition(200, 150, 10)#设置相机位置
    aCamera.SetFocalPoint(0, 0, 0)#设置相机焦点
    aCamera.ComputeViewPlaneNormal()
    aCamera.Azimuth(30.0)
    aCamera.Elevation(30.0)

    # Add renderer to renderwindow and render
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    ren.SetActiveCamera(aCamera)
    ren.ResetCamera()
    #aCamera.Dolly(1.5)
    renWin.SetSize(640, 480)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.SetBackground(colors.GetColor3d("BkgColor"))
    renWin.Render()

    # imgName = "img.png"
    # WriteImage(imgName, renWin, rgba=False)

    iren.Initialize()
    iren.Start()

def WriteImage(fileName, renWin, rgba=True):
    """
    Write the render window view to an image file.

    Image types supported are:
     BMP, JPEG, PNM, PNG, PostScript, TIFF.
    The default parameters are used for all writers, change as needed.

    :param fileName: The file name, if no extension then PNG is assumed.
    :param renWin: The render window.
    :param rgba: Used to set the buffer type.
    :return:
    """

    import os

    if fileName:
        # Select the writer to use.
        path, ext = os.path.splitext(fileName)
        ext = ext.lower()
        if not ext:
            ext = '.png'
            fileName = fileName + ext
        if ext == '.bmp':
            writer = vtk.vtkBMPWriter()
        elif ext == '.jpg':
            writer = vtk.vtkJPEGWriter()
        elif ext == '.pnm':
            writer = vtk.vtkPNMWriter()
        elif ext == '.ps':
            if rgba:
                rgba = False
            writer = vtk.vtkPostScriptWriter()
        elif ext == '.tiff':
            writer = vtk.vtkTIFFWriter()
        else:
            writer = vtk.vtkPNGWriter()

        windowto_image_filter = vtk.vtkWindowToImageFilter()
        windowto_image_filter.SetInput(renWin)
        windowto_image_filter.SetScale(1)  # image quality
        if rgba:
            windowto_image_filter.SetInputBufferTypeToRGBA()
        else:
            windowto_image_filter.SetInputBufferTypeToRGB()
            # Read from the front buffer.
            windowto_image_filter.ReadFrontBufferOff()
            windowto_image_filter.Update()

        writer.SetFileName(fileName)
        writer.SetInputConnection(windowto_image_filter.GetOutputPort())
        writer.Write()
    else:
        raise RuntimeError('Need a filename.')


if __name__ == '__main__':
    main()

