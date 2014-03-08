"""
Mobile Data Coversion Kit

This is a class wrote to handing the CSV parsing

Author: Jon Nordling, Michael Humber 
Date: 8/8/2013
Version 1.1

Compatible with Python versions 2.6x to 3.0


"""
import csv
class Csv_parser:
	def __init__(self,cfile):
		self.x = str(cfile)
		self.csv_file = csv.reader(open(cfile),delimiter=',')
		self.csv_rows = []
		self.headers=[]
		self.main()

	def main(self):
		self.create_csv_rows()
	def create_csv_rows(self):
		for row in self.csv_file:
			self.csv_rows.append(row)
	def get_header(self):
		return self.csv_rows[0]
	def get_number_rows(self):
		row_count = len(self.csv_rows)-1
		return row_count
	def get_number_attributes(self):
		return len(self.get_header())
