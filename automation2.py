#!/usr/bin/env python
# coding: utf-8

# In[80]:


#author Håkon Hegreberg
import os
import sys
import time, datetime
import arcpy
from zipfile import ZipFile
from login_utils import password, user
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
from time import strftime
from shutil import copyfile



# Workspace
# 

# In[81]:


arcpy.env.workspace = "C:/ProgramData/Anaconda3/envs/KDE/default.gdb"
arcpy.env.overwriteOutput = True

#for å lage ny env
#out_folder_path = "C:/ProgramData/Anaconda3/envs/KDE" 
#out_name = ""
#arcpy.CreateFileGDB_management(out_folder_path, out_name)


# # GPX TO shape and LINE
# 

# In[82]:



#f = r"C:/Users/hauke/test/bachelor/f"


#GPX filer
gpx_filepath = r"C:\Users\hauke\bacherlor2020\gpxfiler"



lineField = ""
sortField = ""

gpx_list = os.listdir(gpx_filepath)

for gpx_file in gpx_list:
    if gpx_file.endswith(".gpx"):
        full_gpx_path = os.path.join(gpx_filepath, gpx_file)
        output_shapefile = os.path.splitext(full_gpx_path)[0] + ".shp"
        try:
            arcpy.GPXtoFeatures_conversion(full_gpx_path, output_shapefile)
        except Exepction as e:
            print(e)
        try:
            arcpy.PointsToLine_management(output_shapefile, gpx_filepath + gpx_file, lineField, sortField)
        except Exception as e:
            print(e)

    

print("finished all converting all gpx to shapefile")


# # Points to line

# In[83]:



#for shp_file in shp_list:
#    if shp_file.endswith(".shp"):
#        full_shp_path = os.path.join(shp_filepath, shp_file)
#        output_shapefile1 = os.path.splitext(full_shp_path)[0] + ".shp"
#        #arcpy.PointsToLine_management(output_shapefile, gpx_filepath + shp_file, 'name')
#        arcpy.PointsToLine_management(output_shapefile, gpx_filepath + gpx_file, lineField, sortField)
#print("finished all converting points to lines")
    


# 
# # Merged Lines

# In[84]:



arcpy.env.workspace = r"C:\Users\hauke\bacherlor2020\linjer"

fc = arcpy.ListFeatureClasses(feature_type = 'line')

#output = r"C:/Users/hauke/test/bachelor/f/merged.shp"
output = r"C:\Users\hauke\bacherlor2020\merged_lines\merged.shp"

addSourceInfo = "test"
arcpy.Merge_management(fc, output, addSourceInfo)


#    # Buffer merged lines

# In[85]:



arcpy.env.workspace = r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb"
arcpy.env.overwriteOutput = True
#output = r"C:\Users\hauke\bacherlor2020\merged_lines\merged.shp"


in_features = output
out_feature_class =  r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb/buffer7_5m"



arcpy.Buffer_analysis(in_features,
                      out_feature_class,
                      buffer_distance_or_field="7 Meters",
                      line_side="FULL",
                      line_end_type="ROUND",
                      dissolve_option="NONE",
                      dissolve_field=[],
                      method="PLANAR")


# # Aggregate Polygons
# 

# In[86]:


arcpy.env.workspace = r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb"
arcpy.env.overwriteOutput = True

#buffer = r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb/buffer4"
buffer = out_feature_class
buffer_AggregatePolygons = r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb/buffer3_aggregated"
buffer_AggregatePolygons_Tbl = "yikes"




arcpy.cartography.AggregatePolygons(in_features=buffer,
                                    out_feature_class=buffer_AggregatePolygons,
                                    aggregation_distance="20 Meters",
                                    minimum_area="0 Unknown",
                                    minimum_hole_size="0 Unknown",
                                    orthogonality_option="NON_ORTHOGONAL",
                                    barrier_features=[],
                                    out_table=buffer_AggregatePolygons_Tbl,
                                    aggregate_field="")


# # Polygon to Centerline
# 

# In[95]:



inputLyr = r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb/buffer3_aggregated"
out_feature_class1 = r"C:/ProgramData/Anaconda3/envs/KDE/default.gdb/centerline_aggregated1"
arcpy.topographic.PolygonToCenterline(inputLyr, out_feature_class1)
arcpy.env.overwriteOutput = True


# # Trim Lines

# In[96]:


arcpy.TrimLine_edit(out_feature_class1, "150 Meters", "DELETE_SHORT")


# # Feature to shape

# In[97]:




centerline_aggregated1 = out_feature_class1
senterlinje_2_ = r"C:\Users\hauke\bacherlor2020\senterlinje"
senterlinje = arcpy.conversion.FeatureClassToShapefile(Input_Features=[centerline_aggregated1],
                                                       Output_Folder=senterlinje_2_)


# # Featurelayer - GDB(ONLINE)

# In[98]:


from arcgis.gis import GIS
gis = GIS('Home')

# path relative to this notebook
data_dir = r"C:\Users\hauke\bacherlor2020\senterlinje"

#Get list of all files
file_list = os.listdir(data_dir)

#Filter and get only .sd files
sd_file_list = [x for x in file_list if x.endswith(".shp")]
print("Number of .shp files found: " + str(len(sd_file_list)))



#arcgisoneline login
gis = GIS('https://ntnu-gis.maps.arcgis.com/', user, password)

#variables
itemid = '697baf4054c147339c544f0b782e4134'
upload_zip = r"C:\Users\hauke\bacherlor2020\senterlinje\sipsip.zip"
dld_path = r'C:\Users\hauke\test\bachelor\f'


# create a ZipFile object
zipObj = ZipFile(r'C:\Users\hauke\bacherlor2020\senterlinje\sipsip.zip', 'w')
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.cpg")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.dbf")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.prj")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.sbn")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.sbx")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.shp")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.shp.xml")
zipObj.write(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.shx")
zipObj.close()
#print login
un = gis.properties.user.username
print('Logged in as : {}'.format(un))                       

#overwrite feature host layer
dataitem = gis.content.get(itemid)
flc = FeatureLayerCollection.fromitem(dataitem)
flc.manager.overwrite(upload_zip)




# # remove shapefiles

# In[99]:


os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.cpg")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.dbf")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.prj")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.sbn")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.sbx")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.shp")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.shp.xml")
os.remove(r"C:\Users\hauke\bacherlor2020\senterlinje\centerline_aggregated1.shx")


# In[ ]:





# In[ ]:





# # Raster to Polygon

# In[ ]:



    


# # Polygon to Centerline

# In[ ]:





# 

# In[ ]:





# 

# In[ ]:





# In[ ]:




