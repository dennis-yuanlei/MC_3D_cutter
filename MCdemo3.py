#-*- coding: utf-8 -*-
# author:yuan_lei
# datetime:2019/7/18 20:24


import vtk


def main():
    colors = vtk.vtkNamedColors()

    colors.SetColor("SkinColor", [72, 209, 204, 255])#设置图像颜色
    colors.SetColor("BkgColor", [51, 77, 102, 255])#设置背景颜色

    # Create the renderer, the render window, and the interactor. The renderer
    # draws into the render window, the interactor enables mouse- and
    # keyboard-based interaction with the data within the render window.
    #
    aRenderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(aRenderer)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    #############################################################
    #读取PNG图像，必须是灰度图像

    reader = vtk.vtkPNGReader()
    reader.SetFileDimensionality(2)#存储在文件中的维数
    reader.SetFilePrefix("E:\PYproject\BrainConnect/allen_data/img512/s") #指定图像文件的前缀
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
    skinExtractor.SetValue(0, 170)
    #**************************************************************************

    #保存VTK,这段代码有问题
    # vtkWriter = vtk.vtkPolyDataWriter()
    # vtkWriter.SetInputData(skinExtractor.GetOutput())
    # vtkWriter.SetFileName("3Dbrain.vtk")
    # vtkWriter.Update()
    # vtkWriter.Delete()
    #

    skinStripper = vtk.vtkStripper()
    skinStripper.SetInputConnection(skinExtractor.GetOutputPort())
    # skinStripper.Update()

    skinMapper = vtk.vtkPolyDataMapper()
    skinMapper.SetInputConnection(skinStripper.GetOutputPort())
    skinMapper.ScalarVisibilityOff()

    skin = vtk.vtkActor()#actor表示渲染场景中的实体
    skin.SetMapper(skinMapper)
    skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))#vtkProperty是一个对象，表示几何对象的光照和其他表面属性，主要是颜色，镜面反射，不透明度等
    skin.GetProperty().SetSpecular(.3)
    skin.GetProperty().SetSpecularPower(20)

    # An isosurface, or contour value of 1150 is known to correspond to the
    # bone of the patient.
    # The triangle stripper is used to create triangle strips from the
    # isosurface these render much faster on may systems.
    boneExtractor = vtk.vtkMarchingCubes()
    boneExtractor.SetInputConnection(reader.GetOutputPort())
    boneExtractor.SetValue(0, 80)

    boneStripper = vtk.vtkStripper()
    boneStripper.SetInputConnection(boneExtractor.GetOutputPort())

    boneMapper = vtk.vtkPolyDataMapper()
    boneMapper.SetInputConnection(boneStripper.GetOutputPort())
    boneMapper.ScalarVisibilityOff()

    bone = vtk.vtkActor()
    bone.SetMapper(boneMapper)
    bone.GetProperty().SetDiffuseColor(colors.GetColor3d("Ivory"))

    # An outline provides context around the data.
    #
    outlineData = vtk.vtkOutlineFilter()#vtkOutlineFilter是一个过滤器，用于生成任何数据集或复合数据集的线框轮廓。轮廓由数据集边界框的十二个边组成。
    #此边界框只是将数据的边界框出来，框的大小不是由该函数决定，由数据本身的边界决定
    outlineData.SetInputConnection(reader.GetOutputPort())

    mapOutline = vtk.vtkPolyDataMapper()
    mapOutline.SetInputConnection(outlineData.GetOutputPort())

    outline = vtk.vtkActor()
    outline.SetMapper(mapOutline)
    outline.GetProperty().SetColor(colors.GetColor3d("Black"))

    # Now we are creating three orthogonal planes passing through the
    # volume. Each plane uses a different texture map and therefore has
    # different coloration.

    # Start by creating a black/white lookup table.
    bwLut = vtk.vtkLookupTable()
    bwLut.SetTableRange(0, 2000)
    bwLut.SetSaturationRange(0, 0)
    bwLut.SetHueRange(0, 0)
    bwLut.SetValueRange(0, 1)
    bwLut.Build()  # effective built

    # Now create a lookup table that consists of the full hue circle
    # (from HSV).
    hueLut = vtk.vtkLookupTable()
    hueLut.SetTableRange(0, 2000)
    hueLut.SetHueRange(0, 1)
    hueLut.SetSaturationRange(1, 1)
    hueLut.SetValueRange(1, 1)
    hueLut.Build()  # effective built

    # Finally, create a lookup table with a single hue but having a range
    # in the saturation of the hue.
    satLut = vtk.vtkLookupTable()
    satLut.SetTableRange(0, 2000)
    satLut.SetHueRange(.6, .6)
    satLut.SetSaturationRange(0, 1)
    satLut.SetValueRange(1, 1)
    satLut.Build()  # effective built

    # Create the first of the three planes. The filter vtkImageMapToColors
    # maps the data through the corresponding lookup table created above.  The
    # vtkImageActor is a type of vtkProp and conveniently displays an image on
    # a single quadrilateral plane. It does this using texture mapping and as
    # a result is quite fast. (Note: the input image has to be unsigned char
    # values, which the vtkImageMapToColors produces.) Note also that by
    # specifying the DisplayExtent, the pipeline requests data of this extent
    # and the vtkImageMapToColors only processes a slice of data.
    sagittalColors = vtk.vtkImageMapToColors()
    sagittalColors.SetInputConnection(reader.GetOutputPort())
    sagittalColors.SetLookupTable(bwLut)
    sagittalColors.Update()

    sagittal = vtk.vtkImageActor()
    sagittal.GetMapper().SetInputConnection(sagittalColors.GetOutputPort())
    sagittal.SetDisplayExtent(255, 255, 0, 511, 0, 131)

    # Create the second (axial) plane of the three planes. We use the
    # same approach as before except that the extent differs.
    axialColors = vtk.vtkImageMapToColors()
    axialColors.SetInputConnection(reader.GetOutputPort())
    axialColors.SetLookupTable(hueLut)
    axialColors.Update()

    axial = vtk.vtkImageActor()
    axial.GetMapper().SetInputConnection(axialColors.GetOutputPort())
    axial.SetDisplayExtent(0, 511, 0, 511, 65, 65)

    # Create the third (coronal) plane of the three planes. We use
    # the same approach as before except that the extent differs.
    coronalColors = vtk.vtkImageMapToColors()
    coronalColors.SetInputConnection(reader.GetOutputPort())
    coronalColors.SetLookupTable(satLut)
    coronalColors.Update()

    coronal = vtk.vtkImageActor()
    coronal.GetMapper().SetInputConnection(coronalColors.GetOutputPort())
    coronal.SetDisplayExtent(0, 511, 255, 255, 0, 131)


    # It is convenient to create an initial view of the data. The FocalPoint
    # and Position form a vector direction. Later on (ResetCamera() method)
    # this vector is used to position the camera to look at the data in
    # this direction.
    aCamera = vtk.vtkCamera()
    aCamera.SetViewUp(0, 0, -1)
    aCamera.SetPosition(0, -1, 0)
    aCamera.SetFocalPoint(0, 0, 0)
    aCamera.ComputeViewPlaneNormal()
    aCamera.Azimuth(30.0)
    aCamera.Elevation(30.0)

    # Actors are added to the renderer. An initial camera view is created.
    # The Dolly() method moves the camera towards the FocalPoint,
    # thereby enlarging the image.
    aRenderer.AddActor(outline)
    aRenderer.AddActor(skin)
    aRenderer.AddActor(bone)
    aRenderer.AddActor(sagittal)
    aRenderer.AddActor(axial)
    aRenderer.AddActor(coronal)

    # Set skin,bone to semi-transparent.
    skin.GetProperty().SetOpacity(0.3)
    bone.GetProperty().SetOpacity(0.1)

    aRenderer.SetActiveCamera(aCamera)
    aRenderer.ResetCamera()
    aCamera.Dolly(1.5)

    # Set a background color for the renderer and set the size of the
    # render window (expressed in pixels).
    aRenderer.SetBackground(colors.GetColor3d("BkgColor"))
    renWin.SetSize(640, 480)#设置显示窗口大小

    # Note that when camera movement occurs (as it does in the Dolly()
    # method), the clipping planes often need adjusting. Clipping planes
    # consist of two planes: near and far along the view direction. The
    # near plane clips out objects in front of the plane the far plane
    # clips out objects behind the plane. This way only what is drawn
    # between the planes is actually rendered.
    aRenderer.ResetCameraClippingRange()

    # Initialize the event loop and then start it.
    iren.Initialize()
    iren.Start()



if __name__ == '__main__':
    main()