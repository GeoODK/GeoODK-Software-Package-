   ###### Mobile Data Conversion Kit  #######

   Author: Jon Nordling
   Revised: August 8, 2013

   Copyright (C) 2013 University of Maryland. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ######### SIMPLEKML  ############

   Mobile Data Conversion Kit Package inlucdes simplekml model: 
   simplekml is a python package which enables you to generate KML with as little effort as possible.

   There were no modifications to the files.

   See the http://simplekml.readthedocs.org for usage and reference.
   Visit http://code.google.com/p/simplekml/ for the homepage.

   ###### PYSHP: Python Shapefile Library ########

      /src/shapefile.py

	Note: One one additional funtion way added. See /src/shapefile.py to Read more.

      Python Shapefile Library

      This was used in the mobile data conversion kit for creating shape files.
   ========================

   :Author: Joel Lawhead - jlawhead@geospatialpython.com

   :Revised: June 23, 2013

   .. contents::

   Overview
   --------

   The Python Shapefile Library (pyshp) provides read and write support for the Esri
   Shapefile format. The Shapefile format is a popular Geographic Information
   System vector data format created by Esri.  For more information about this format 
   please read the well-written "ESRI Shapefile Technical Description - July 1998"
   located at http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf.  
   The Esri document describes the shp and shx file formats.  However a third file
   format called dbf is also required.  This format is documented on the web as the
   "XBase File Format Description" and is a simple file-based database format created
   in the 1960's.  For more on this specification see: 
   http://www.clicketyclick.dk/databases/xbase/format/index.html   

   Both the Esri and XBase file-formats are very simple in design and
   memory efficient which is part of the reason the shapefile format remains popular
   despite the numerous ways to store and exchange GIS data available today. 

   Pyshp is compatible with Python 2.4-3.x.

   This document provides examples for using pyshp to read and write shapefiles.  

   Currently the sample census blockgroup shapefile referenced in the examples is
   only available on the google code project site at http://code.google.com/p/pyshp.
   These examples are straight-forward and you can also easily run them against your 
   own shapefiles manually with minimal modification. Other examples for specific 
   topics are continually added to the pyshp wiki on google code and the blog
   http://GeospatialPython.com.

   Important: For information about map projections, shapefiles,
   and Python please visit: http://code.google.com/p/pyshp/wiki/MapProjections

   I sincerely hope this library eliminates the mundane distraction of simply 
   reading and writing data, and allows you to focus on the challenging and FUN
   part of your geospatial project. 