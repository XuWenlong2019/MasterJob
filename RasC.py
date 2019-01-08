"""
时间：2018年12月25日
作者：许文龙
目的：多期空间数据逐像元分析
任务：1982-2015年的年平均最大合成NDVI数据与时间顺序的一元线性回归
"""

# Import system modules
import os,time
import utils
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import gdal_array

# 初始时间锁
StartTime = time.clock()
# 设置工作目录
os.chdir(r"F:\MyJob\Data\GIMMS_NDVI3g_v1\TP_TIF_YEAR_GIMMS_MEAN")
# 输入栅格为多波段栅格，前期将多期NDVI数据合成，注意投影和压缩（Data Management Tools - Raster - Raster Processing - Composite Bands）
ndviRaster = "TP_GIMMS_NDVI.TIF"
outRaster = "TP_GIMMS_NDVI_GRC.TIF"
# 读入栅格数据
raster = gdal.Open(ndviRaster)
# 获取栅格数据波段数
bandNum = raster.RasterCount
# 获取栅格数据列数
colNum = raster.RasterXSize
# 获取栅格数据行数
rowNum = raster.RasterYSize
"""
# 获取栅格数据仿射矩阵（Top Left X、W-E pixel resolution、Rotation、Top Left Y、Rotation、N-S pixel resolution）
geotransinfo = raster.GetGeoTransform()
# 获取栅格数据投影信息
projinfo = raster.GetProjection()
"""
x = np.arange(1, bandNum + 1)
rasIV = np.zeros((rowNum * colNum, bandNum), dtype=np.float32)
for i in range(1, bandNum + 1):
    data = raster.GetRasterBand(i).ReadAsArray()
    data.shape = (rowNum * colNum, 1)
    rasIV[:, i - 1] = data[:, 0]
"""
rasSlope = np.zeros((rowNum * colNum, 1), dtype=np.float32)
for i in range(0, rowNum * colNum):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, rasIV[i, : ])
    if p_value > 0.05:
        rasSlope[i, 0] = np.NAN
    else:
        rasSlope[i, 0] = slope
rasSlope.shape = (rowNum, colNum)
out = gdal_array.SaveArray(rasSlope,outRaster,format = "GTiff",prototype = ndviRaster)
out = None
"""
rasSlope = np.zeros((rowNum * colNum, 1), dtype=np.float32)
for i in range(0, rowNum * colNum):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, rasIV[i, : ])
    rasSlope[i, 0] = slope
rasSlope.shape = (rowNum, colNum)
out = gdal_array.SaveArray(rasSlope,outRaster,format = "GTiff",prototype = ndviRaster)
out = None
# 终止时间锁
EndTime = time.clock()
# 运行时间
print('Running time: %s Seconds' % (EndTime-StartTime))