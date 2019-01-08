"""
Created on Sat Jan 20 16:19:08 2018

@author: XuWenlong

"""

import sys,os 
from osgeo import osr,ogr,gdal
import numpy as np
from pyhdf.SD import *

os.chdir("D:\\Workspace\\Python_workspace\\trmm")  #设置工作目录

#提取文件夹中的HDF格式数据文件
def file_name(file_dir):
	file_hdf=[]
	for root, dirs, files in os.walk(file_dir):
		for file in files:
			if os.path.splitext(file)[1] == '.HDF':
				file_hdf.append(os.path.join(root, file))
	return file_hdf

#将HDF格式文件转换为TIFF格式文件
def hdf2tiff(file):
	hdf = SD(file)  #打开HDF文件
	attr = hdf.attributes(full=1)  #HDF文件属性字典
	attNames = attr.keys()
	attNames.sort()
	for name in attNames:
		t = attr[name]
		print name,t

	dsets = hdf.datasets()  #HDF数据字典
	dsNames = dsets.keys()
	dsNames.sort()
	for name in dsNames:
		ds = hdf.select(name)
		vAttr = ds.attributes()
		t = dsets[name]
		print name,vAttr,t

	im_data = hdf.select('precipitation').get()*3
	im_data = np.fliplr(im_data)
	im_data = np.transpose(im_data)
	np.putmask(im_data,im_data<0,np.nan)
	im_width = 1440
	im_height = 400
	im_bands = 1
	datatype = gdal.GDT_UInt16
	sr = osr.SpatialReference()
	sr.ImportFromEPSG(4326)
	im_proj = sr.ExportToWkt()
	im_geotrans = (-180,0.25,0,50,0,-0.25)
	driver = gdal.GetDriverByName("GTiff")
	dataset = driver.Create(os.path.splitext(file)[0]+".TIF",im_width, im_height, im_bands, datatype)
	dataset.SetGeoTransform(im_geotrans)
	dataset.SetProjection(im_proj)
	dataset.GetRasterBand(1).WriteArray(im_data)
	del dataset
	hdf.end()

for file in file_name(os.getcwd()):
	hdf2tiff(file)













