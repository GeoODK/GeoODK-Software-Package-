"""
Mobile Data Coversion Kit

Provides write support for CSV Google kmz
This script uses a thirdparty module simplekml.
See README.txt for more information

Author: Jon Nordling, Michael Humber 
Date: 8/8/2013
Version 1.1

Compatible with Python versions 2.6x to 3.0


"""
import os
import sys
import simplekml
from Csv_parser import *
import sys



def kmz_main(output_dir,csvfile,lat,lng,output_name):
	output_name= output_name.replace('.csv','')
	output_dir = output_dir + '/'
	x= Csv_parser(csvfile)
	fields = x.get_header()			# Fields is an array of the header attributes

	for i in range(len(fields)):
		if fields[i] == lat:
			lat_index = i
		if fields[i] == lng:
			lng_index = i

	#print lat_index, lng_index # The lat and long index in the array
	kml = simplekml.Kml()

	for j in range(len(x.csv_rows)):
		if (j == 0):
			continue
		else:
			if (x.csv_rows[j][lat_index] !='null') or (x.csv_rows[j][lng_index]!='null'):
				#print x.csv_rows[j][lat_index],x.csv_rows[j][lng_index]

				lat_cord = x.csv_rows[j][lat_index]
				lng_cord = x.csv_rows[j][lng_index]
				pnt = kml.newpoint(coords=[(lng_cord , lat_cord)])
				#pnt.name = 'Point '+str(x.csv_rows[j])
				descript = "<table border=\'1\'><th>Attributes</th><th>Value</th>"
				for h in range(len(x.csv_rows[j])):
					#pnt.description = str(fields[h])+' : '+str(x.csv_rows[j][h])+'<br />'
					descript=descript+'<tr><td><strong>'+fields[h]+'</strong></td>'+'<td>'+x.csv_rows[j][h]+'</td>'+'</tr>'
					#print fields[h]
				pnt.description = descript+'</table>'
	kml.savekmz(output_dir+output_name+'.kmz')




#kmz_main(lat,lng,file_full,output_name)
			

			



