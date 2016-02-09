#Script for Lab 2
#By Thomas Ryan
#For Geog 458

#Import modules
import arcpy
import sys
import os
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')

#Single varible for changing path names and setting workspace
workspace = r"C:\Users\Thomas\Downloads\Geog 458 Lab 2\\"
arcpy.env.workspace = workspace
env.overwriteOutput = True

#Grabbing inputfiles
mytable = workspace + r"King\King.shp\\"
reclasstable = workspace + r"ReclassTableExample.dbf\\"

#Taking user input
infield = input("Enter the name of the field you want to reclassify: ")
outfield = input("Enter the name of the new field: ")
usenotfoundvalue = True

#Defining the function of the notfoundvalue input varible
notfoundvalue = input("Do you want to assign a placeholder for values outside of the reclassification range?")
if notfoundvalue == "Yes" or "yes" or "y" or "ye":    
    notfoundvalue = input("Enter placeholder for values outside of the classification range: ")
elif notfoundvalue == "No" or "no" or "n" or "na":
    usenotfoundvalue = False
else:
    notfoundvalue = input("Do you want to assign a placeholder for values outside of the reclassification range?")

#Creating outfield and input shapefile cursor
arcpy.AddField_management(cur_shapefile, outfield, "DOUBLE", "")
mytable_cursor = arcpy.da.UpdateCursor(mytable,[infield, outfield])

#Looping through the input shapefile
for cur_row in mytable_cursor:
    #Looping through the classification table
    reclasstable_cursor = arcpy.da.UpdateCursor(reclasstable,["lowerbound", "upperbound", "value"])
    updated = False
    
    for cur_value in reclasstable_cursor:
        #Reclassifiying
        if cur_row[0] >= cur_value[0] and cur_row[0] <= cur_value[1]:
                
            cur_row[1] = cur_value[2]
            mytable_cursor.updateRow(cur_row)
            updated = True
    #Clean up
    del reclasstable_cursor
    #Checking whether or not to use the notfoundvalue
    if not updated:
        if usenotfoundvalue:
            cur_row[1] = notfoundvalue
        else:
            cur_row[1] = cur_row[0]
#Clean up    
del mytable_cursor
