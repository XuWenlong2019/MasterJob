# -*- coding: utf-8 -*-
"""
Created on Fri May 19 22:15:13 2017

@author: XuWenlong
"""

import os
import math
import xlrd,xlwt
import numpy as np

def MK_trend(x):
    s=0
    length=len(x)
    #print length
    for m in range(0,length-1):
        for n in range(m+1,length):
            if x[n]>x[m]:
                s=s+1
            elif x[n]==x[m]:
                s=s+0
            else:
                s=s-1
    #计算vars
    vars=length*(length-1)*(2*length+5)/18
    #计算zc
    if s>0:
        zc=(s-1)/math.sqrt(vars)
    elif s==0:
        zc=0
    else:
        zc=(s+1)/math.sqrt(vars)

    return zc

#设置工作路径
os.chdir("D:\\Workspace\\PPT\\Python_GIS\\pythonMK\\MK")   #修改当前工作路径（第一步）
#os.chdir(r"D:\Workspace\PPT\pythonMK\MK")
#os.chdir("D:/Workspace/PPT/pythonMK/MK") 



data=xlrd.open_workbook("data.xlsx")    #输入文件名（第二步）
table= data.sheets()[0]

nrows=table.nrows   #行数
ncols=table.ncols	#列数

x=[]
zcs=[]
for i in range(1,ncols):
    for j in range(2,nrows):
        cell=table.cell(j,i).value
        if cell != "":
            x.append(cell)
    mk=MK_trend(x)
    #print mk
    zcs.append(mk)
    x=[]


book = xlwt.Workbook() 
sheet = book.add_sheet('sheet1',cell_overwrite_ok=True)
for l in range (0,len(zcs)):
    sheet.write(0,l,zcs[l])
"""	
	if zcs[l]<0:
		sheet.write(1,l,"down")
	elif zcs[l]>0:
		sheet.write(1,l,"up")
	else:
		sheet.write(1,l,"no")
	if abs(zcs[l])>2.32:
		sheet.write(2,l,"99%")
	elif abs(zcs[l])>1.96:
		sheet.write(2,l,"95%")
	elif abs(zcs[l])>1.28:
		sheet.write(2,l,"90%")
	else:
		sheet.write(2,l,"no")
"""
book.save("result.xls")    #保存结果（第三步）