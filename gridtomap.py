import arcpy,os
from arcpy import env
from osgeo import gdal

os.chdir("D:\\Workspace\\Python_workspace\\ndvi2000-2010")
out_path = "D:\\Workspace\\Python_workspace\\ndvi2000-2010\\MAP\\"
env.workspace = "D:\\Workspace\\Python_workspace\\ndvi2000-2010"
Raster_Grid = arcpy.ListRasters("*","GRID")
for raster in Raster_Grid:
    print raster
    gdal.Translate(out_path  + raster.encode('raw_unicode_escape') + ".map",raster.encode('raw_unicode_escape'),format = "PCRaster",outputType = gdal.GDT_Float32)
    print raster.encode('raw_unicode_escape') +  " to PCRaster map"
print "END"