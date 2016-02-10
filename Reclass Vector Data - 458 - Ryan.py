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
arcpy.env.overwriteOutput = True

#Grabbing inputfiles
#@String Pathnames
mytable = arcpy.GetParameterAsText(0)
reclasstable = arcpy.GetParameterAsText(1)
#@String fieldnames
infield = arcpy.GetParameterAsText(2)
outfield = arcpy.GetParameterAsText(3)
#@Integer
usenotfoundvalue = arcpy.GetParameterAsText(4)
#@Boolean
notfoundvalue = arcpy.GetParameterAsText(5)
#@String Pathname
outputfile = arcpy.GetParameterAsText(6)

#For intial testing
#mytable = workspace + "King\\King.shp\\"
#reclasstable = workspace + "ReclassTableExample.dbf\\"
#infield = "PopDens12"
#outfield = "Pop12Cat"
#notfoundvalue = 9999

#Creating outfield and input shapefile cursor
arcpy.CopyFeatures_management(mytable, outputfile)
arcpy.AddField_management(outputfile, outfield, "DOUBLE", "")
mytable_cursor = arcpy.da.UpdateCursor(outputfile,[infield, outfield])

#Looping through the input shapefile
for cur_row in mytable_cursor:
    #Looping through the classification table
    reclasstable_cursor = arcpy.da.UpdateCursor(reclasstable,["lowerbound", "upperbound", "value"])
    updated = False
    
    for cur_value in reclasstable_cursor:
        #Reclassifiying
        if cur_row[0] >= cur_value[0] and cur_row[0] <= cur_value[1]:
                
            cur_row[1] = cur_value[2]
            updated = True
            print "Reclassified"
    #Clean up
    del reclasstable_cursor
    #Checking whether or not to use the notfoundvalue
    if not updated:
        if usenotfoundvalue:
            cur_row[1] = notfoundvalue
            print "Used notfoundvalue of " + str(notfoundvalue)
        else:
            cur_row[1] = cur_row[0]
            print "Used orginal value of " + str(cur_row[0])

    mytable_cursor.updateRow(cur_row)
        
#Clean up    
del mytable_cursor
