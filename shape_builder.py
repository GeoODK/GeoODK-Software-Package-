"""
Mobile Data Coversion Kit

Provides write support for CSV ESRI Shapefiles

Author: Jon Nordling, Michael Humber 
Date: 8/8/2013
Version 1.1

Compatible with Python versions 2.6x to 3.0

"""

import shapefile
import csv
from Csv_parser import *

#import sys

#output_name = sys.argv[1]
#lat = sys.argv[2]
#lng=  sys.argv[3]
#output_dir= sys.argv[4]+'/'
#file_full= sys.argv[5]

#create_shape(output_name,lat,lng,output_dir,file_full)

def create_shape(cfile,lat_field,lng_field,output_dir,file_full):
	output_shape = cfile.replace('.csv','')
	output_dir = output_dir +'/'
	projection = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	csv_file = Csv_parser(file_full)
	headers = csv_file.get_header()
	headers_char = [0]*len(headers)
	csv_rows=csv_file.csv_rows
	lat_index = csv_rows[0].index(lat_field)
	lng_index = csv_rows[0].index(lng_field)
	#print lat_index, lng_index
	
	shape_file = shapefile.Writer(shapefile.POINT)

	for h in csv_rows:
		for g in range(len(h)):
			if len(h[g]) >headers_char[g]:
				headers_char[g] = len(h[g])

	for i in range(len(headers)):
		shape_file.field(headers[i], 'C', headers_char[i])

	for row in csv_rows:
		if (row[lat_index] =="null" or row[lng_index]=="null"):
			continue
		else:
			if row !=headers:
				shape_file.point(float(row[lng_index]), float(row[lat_index]))
				shape_file.recordFromList(row)

	
	shape_file.save(output_dir+output_shape)
	proj_file = open(output_dir+output_shape+'.prj','w')
	proj_file.write(projection)
	proj_file.close()



#create_shape(output_name,lat,lng,output_dir,file_full)