"""
Mobile Data Coversion Kit

Provides a way to download the images from the links in the CSV file

Author: Jon Nordling
Date: 8/8/2013
Version 1.1

Compatible with Python versions 2.6x to 3.0


"""

import urllib
import sys

# This module was written to hand the csv parsing
from Csv_parser import *

#full_file = sys.argv[1]
#image_f = sys.argv[2]
#out_put = sys.argv[3]
#download_images(full_file, image_f,out_put)

def download_images(c_file, image_field,output_dir):

	csv_file = Csv_parser(c_file)
	headers = csv_file.get_header()
	csv_rows = csv_file.csv_rows
	img_index = csv_rows[0].index(image_field)

	#print img_index
	count =1
	for i in csv_rows:
		if (i[img_index] ==image_field) or (i[img_index]=='null'):
			count = count +1
			continue
		else:
			#print i[img_index]
			url = i[img_index]
			f = urllib.urlopen(url)
			localFile = open(output_dir+'/image_'+str(count)+'.jpg', 'wb')
			localFile.write(f.read())
			localFile.close()
			f.close()
			count = count +1


#download_images(full_file, image_f,out_put)