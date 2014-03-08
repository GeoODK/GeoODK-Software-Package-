"""
Mobile Data Coversion Kit

Provides read and write support for ESRI Shapefiles, Google KMZ Files
and will download images locally from the links in the CSV file.
This file is the main file to run.

Author: Jon Nordling
Date: 8/8/2013
Version 1.1

Compatible with Python versions 2.6x to 3.0


"""

from ttk import *
from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
import csv
import os
import subprocess
import threading
import os
import base64

# This module was written to hand the csv parsing
from Csv_parser import *
from kmz_creater import *
from shape_builder import *
from image_download import *

#from kmz_creater import *

#from error_window import *


class MainFrame:
	def __init__(self, master):
		# Setting the Global varibales and the Master Frame
		#global frame
		#frame = Frame(master)
		#frame.grid()

		################################################################################################
		# HEADER FRAME
		# This is the header frame for the logos and the Header text information
		################################################################################################
		#print os.getcwd()
		#test_image = 'icons\logo2.gif'
		#g = base64.encodestring(open(test_image,"rb").read())
		#testfile = open('image.txt','w')
		#testfile.write(g)
		#testfile.close()
		self.header_frame = Frame(master)
		self.header_frame.grid()		
		try:
			self.photo = PhotoImage(file='icons\logo2.gif')
			self.photo_label = Label(self.header_frame,image=self.photo)
			self.photo_label.image = self.photo # keep a reference!
			self.photo_label.grid(row=0, column=0)
		except:
			self.photo_label = Label(self.header_frame,width=10,height=5)
			self.photo_label.grid(row=0, column=0)


		self.header_label=Label(self.header_frame, text="Mobile Data Conversion Kit",font=("Helvetica", 22),anchor="center")
		self.header_label.grid(row=0,column=1,padx=80)

		step_one_lable = Label(master,text="1) Choose the CSV data file(s) to process:",font=("Helvetica", 13))
		step_one_lable.grid(sticky=W,padx=5)

		#.files_list_full = []

		#################################################################################################
		#FILES FRAME
		# This is a frame that is ment for the collecting a record of the CSV Files to process
		#################################################################################################

		self.files_frame = Frame(master)
		self.files_frame.grid(pady=10)

		self.list_box_frame=Frame(self.files_frame)
		self.list_box_frame.grid(row=0,column=0)

		self.list_box_button_frame= Frame(self.files_frame)
		self.list_box_button_frame.grid(row=0,column=1,sticky=N,padx=20)

		#self.file_listbox = ttk.Treeview(self.list_box_frame,width=55, height=10)
		#self.file_listbox.grid(row=0,column=0)
		tree_columns = ("CSV File", "Status")
		self.file_listbox = Treeview(self.list_box_frame,columns=tree_columns, show="headings",height="5")
		for col in tree_columns:
			self.file_listbox.heading(col, text=col)
			if col == 'CSV File':
				self.file_listbox.column(col,width=320)
			else:
				self.file_listbox.column(col,width=100)
		self.file_listbox.grid(row=0,column=0,sticky=E+W)

		#self.yscroll.grid(row=0, column=1, sticky=N+S)
		#self.file_listbox.configure(yscrollcommand=self.yscroll.set)
		self.file_listbox.bind('<<TreeviewSelect>>', self.get_list)

		#self.xscroll = Scrollbar(self.list_box_frame,command=self.file_listbox.xview,orient=HORIZONTAL)
		#self.xscroll.grid(row=1,column=0,sticky=W+E)
		#self.file_listbox.configure(xscrollcommand=self.xscroll.set)


		# This is the button to open the CSV
		self.get_csv_button = Button(self.list_box_button_frame, text= "Add CSV File(s)", command=self.header_listbox)
		self.get_csv_button.grid(row=0,column=0,sticky=W+E)
		self.get_csv_button2 = Button(self.list_box_button_frame, text= "Remove CSV File(s)", command=self.remove_listbox_item)
		self.get_csv_button2.grid(row=1,column=0,pady=5)

		####################################################################################################
		# Content Frame
		# This is a content frame that is 

		step_two_lable = Label(master,text="2) Select the format of the data:",font=("Helvetica", 13))
		step_two_lable.grid(sticky=W,padx=5)

		self.content_frame = Frame(master,bd=0,relief=SUNKEN)
		self.content_frame.grid(pady=10)

		self.content_left_frame = Frame(self.content_frame,bd=0,relief=SUNKEN)
		self.content_left_frame.grid(row=0,column=0,padx=10,sticky=N)

		self.content_right_frame = Frame(self.content_frame,bd=0,relief=SUNKEN)
		self.content_right_frame.grid(row=0,column=1,padx=40,pady=20,sticky=N+S)

		self.content_submit_frame = Frame(self.content_frame,bd=0,relief=SUNKEN)
		self.content_submit_frame.grid(row=0,column=2,padx=5,pady=20,sticky=N+S)

		self.lat_label = StringVar()
		self.lat_label.set("Choose Latitude Field")
		self.list_headers = [' ']
		self.lat_field = OptionMenu(self.content_left_frame,self.lat_label,*self.list_headers)
		self.lat_field.config(width=20)
		self.lat_field.grid(row=2,column=0,sticky=W+E)

		self.lng_label = StringVar()
		self.lng_label.set("Choose Longitude Field")
		self.lng_field = OptionMenu(self.content_left_frame,self.lng_label,*self.list_headers)
		self.lng_field.config(width=20)
		self.lng_field.grid(row=3,column=0,sticky=W+E)

		#self.odk_format_checkbox = Checkbutton(self.content_left_frame, text= "All fields are the same:")
		#self.odk_format_checkbox.grid(row=1,column=0,sticky=W)

		#self.other_table_lable = Label(self.content_right_frame, text=" ")
		#self.other_table_lable.grid(row=0,column=0,sticky=W)


		#self.orientation_label = StringVar()
		#self.orientation_label.set("Choose Orientation Field")
		#self.orientation_field = OptionMenu(self.content_right_frame,self.orientation_label,*self.list_headers)
		#self.orientation_field.config(width=20)
		#self.orientation_field.grid(row=1,column=0,sticky=W+E)

		self.image_label = StringVar()
		self.image_label.set("Choose Image Field")
		self.image_field = OptionMenu(self.content_right_frame,self.image_label,*self.list_headers)
		self.image_field.config(width=20)
		self.image_field.grid(row=0,column=0,sticky=N+S)

		self.set_field_button = Button(self.content_submit_frame,text="Set Fields",width=15,command=self.set_final_fields)
		self.set_field_button.grid(row=0,column=0,sticky=W+E)



		###################################################################################################
		# Selection Frame
		# This frame is ment for the user to decide what they will be doing with the files. 
		###################################################################################################
		self.step_three_lable = Label(master,text="3) Select outputs to export:",font=("Helvetica", 13))
		self.step_three_lable.grid(sticky=W,padx=5,pady=5)


		self.select_frame = Frame(master)
		self.select_frame.grid()

		self.select_frame_left = Frame(self.select_frame,bd=0,relief=SUNKEN)
		self.select_frame_left.grid(row=0,column=0,padx=10,sticky=N)

		self.select_frame_right =Frame(self.select_frame,bd=0,relief=SUNKEN)
		self.select_frame_right.grid(row=0,column=1,padx=10,sticky=S)


		#select_process = Label(self.select_frame_left, text="Select if used ODK Aggregate Default Format:")
		#select_process.grid(row=0,column=0)


		self.kmlvar = IntVar()
		self.shapevar = IntVar()
		self.downloadvar = IntVar()
		self.kml_buttom = Checkbutton(self.select_frame_left, text= "Create KMZ ",variable=self.kmlvar)
		self.kml_buttom.grid(row=1,column=0,sticky=W)

		self.shape_buttom = Checkbutton(self.select_frame_left, text= "Create Shape File ",variable=self.shapevar)
		self.shape_buttom.grid(sticky=W)

		self.download_img_buttom = Checkbutton(self.select_frame_left, text= "Download Images ",variable=self.downloadvar)
		self.download_img_buttom.grid(sticky=W)


		##########################
		
		self.message_lable = Label(self.select_frame_right,text="Processing Status:",width=35)
		self.message_lable.grid(row=0,column=0,sticky=W)

		self.pb = Progressbar(self.select_frame_right,orient ="horizontal",length = 200, mode="determinate",value=0,maximum=100)
		self.pb.grid(row=1,column=0)

		#self.pb["value"]= 50
		#self.pb.start()

		self.footer_frame = Frame(master)
		self.footer_frame.grid()

		self.output_dir = Button(self.footer_frame,text="Output Directory",width=20,command=self.get_workspace)
		self.output_dir.grid(row=0,column=0,pady=20)


		self.output_dir_entry=Entry(self.footer_frame,width=60)
		self.output_dir_entry.grid(row=0,column=1,pady=20)

		self.footer_button_frames = Frame(master)
		self.footer_button_frames.grid(pady=10)


		self.quit_button = Button(self.footer_button_frames,text="QUIT",command=master.quit,width=15)
		self.quit_button.grid(row=0,column=0,padx=10)

		self.clear_button = Button(self.footer_button_frames,text="Reset",width=15,command=self.clear)
		self.clear_button.grid(row=0,column=1,padx=10)

		self.run_button = Button(self.footer_button_frames,text="Run", command=self.run,width=15)
		self.run_button.grid(row=0,column=2,padx=10)

		self.footer_label0 = Label(self.footer_button_frames,text=" ")
		self.footer_label0.grid(row=1,column=0,columnspan=3)
		
		self.footer_label1 = Label(self.footer_button_frames,text="Powered by GeoODK")
		self.footer_label1.grid(row=2,column=0,columnspan=3)

		self.footer_label2 = Label(self.footer_button_frames,text="Developed at University of Maryland")
		self.footer_label2.grid(row=3,column=0,columnspan=3)
		self.file_tree_full =[]
		#self.file_tree_lable=list()
		self.file_tree_ID=0

	def get_list(self,index):
	    # get selected line index
	    index = self.file_listbox.selection()[0]
	    current_file= self.file_listbox.item(index)['values'][0]
	    for i in range(len(self.file_tree_full)):
	    	if current_file== self.file_tree_full[i][0]:
	    		filename= self.file_tree_full[i][2]
	    csv_file = Csv_parser(filename)
	    headers = csv_file.get_header()
	    self.add_headers_to_menu(headers)

	def add_headers_to_menu(self,header):
		# These allow you to clear and reput the lat/lng dropdowns
		self.lat_field.grid_forget()
		self.lng_field.grid_forget()
		self.image_field.grid_forget()
		index = self.file_listbox.selection()[0]
		current_file= self.file_listbox.item(index)['values'][0]
		color = ''
		for i in range(len(self.file_tree_full)):
			if current_file== self.file_tree_full[i][0]:
				fields= self.file_tree_full[i][-2]
				if fields[0]==0:
					self.lat_label.set("Choose Latitude Field")
					color="firebrick4"
				else:
					self.lat_label.set(fields[0])
					color="chartreuse4"

				if fields[1]==0:
					self.lng_label.set("Choose Longitude Field")
				else:
					self.lng_label.set(fields[1])

				#if fields[2]==0:
				#	self.orientation_label.set("Choose Orientation Field")
				#else:
				#	self.orientation_label.set(fields[2])

				if fields[3]==0:
					self.image_label.set("Choose Image Field")
				else:
					self.image_label.set(fields[3])

		for i in header:
			self.lat_field = OptionMenu(self.content_left_frame,self.lat_label,*header)
			#self.orientation_field = OptionMenu(self.content_right_frame,self.orientation_label,*header)
			self.image_field = OptionMenu(self.content_right_frame,self.image_label,*header)
			self.lng_field = OptionMenu(self.content_left_frame,self.lng_label,*header)
		self.lat_field.config(width=20,fg=color)
		self.lng_field.config(width=20,fg=color)
		self.image_field.config(width=20)

		self.lat_field.grid(row=2,column=0,sticky=W+E)
		self.lng_field.grid(row=3,column=0,sticky=W+E)
		self.image_field.grid(row=0,column=0,sticky=N+S)

	def generate_status(self,csv_file):
		total_num_rec = csv_file.get_number_rows()
		numberorAtt =csv_file.get_number_attributes()
		self.num_records.pack_forget()
		self.num_att.pack_forget()		

		self.num_records = Label(frame,text="Total Records: "+str(total_num_rec)+"\t\t\t\t\t\t",justify=RIGHT)
		self.num_records.pack(after=self.summ_label)
		self.num_att = Label(frame,text="Total Attribute: "+str(numberorAtt)+"\t\t\t\t\t\t",justify=RIGHT)
		self.num_att.pack(after=self.num_records)

	def create_header_list_status(self,file_list,file_label_array):
		start_status = 'Incomplete'		
		for i in range(len(file_list)):
			self.file_tree_full.append([file_label_array[i],start_status,file_list[i],[0,0,0,0],self.file_tree_ID])
			self.file_tree_ID = self.file_tree_ID+1
		return self.file_tree_full

	def file_label_list(self,files):
		file_label_array = []
		for i in files:
			count = 0
			for k in reversed(i):
				if k == '/':
					file_label_array.append(i[-count:])
					break
				count = count+1
		return file_label_array

	def insert_to_tree(self,items):
		x = self.file_listbox.get_children()
		for u in x:
			self.file_listbox.delete(u)
		for i in items:
			self.file_listbox.insert('','end', values=i)

	def header_listbox(self):
		filename = askopenfilename(filetypes=[("allfiles",".csv")],multiple=TRUE)
		files = root.tk.splitlist(filename)
		file_label_array = self.file_label_list(files)
		tree_data=self.create_header_list_status(files,file_label_array)
		self.insert_to_tree(tree_data)

	def find_match_node(self,file_id):
		for i in range(len(self.file_tree_full)):
			if file_id == self.file_tree_full[i][-1]:
				x = self.file_tree_full.index(self.file_tree_full[i])
				self.file_tree_full.pop(x)
				break

		for i in self.file_tree_full:
			print i

	def remove_listbox_item(self):
		index = self.file_listbox.selection()[0]

		#print index		
		current_file_id= self.file_listbox.item(index)['values'][-1]
		self.find_match_node(current_file_id)
		#print current_file
		self.file_listbox.delete(index)

	def get_workspace(self):
		self.output_dir_entry.destroy()
		self.output_dir_entry=Entry(self.footer_frame,width=60)
		self.output_dir_entry.grid(row=0,column=1,pady=20)
		dirc= askdirectory(initialdir=os.getcwd())
		self.output_dir_entry.insert(0,str(dirc))
		#print dirc

	def set_final_fields(self):
		index = self.file_listbox.selection()[0]
		current_file_id= self.file_listbox.item(index)['values'][-1]
		for i in range(len(self.file_tree_full)):
			if self.file_tree_full[i][-1]== current_file_id:
				lat = self.lat_label.get()
				lng = self.lng_label.get()
				img = self.image_label.get()
				#ort = self.orientation_label.get()
				if lat=="Choose Latitude Field":
					self.file_tree_full[i][-2][0]=0
				else:
					self.file_tree_full[i][-2][0]= lat

				if lng=="Choose Longitude Field":
					self.file_tree_full[i][-2][1]= 0
				else:
					self.file_tree_full[i][-2][1]= lng

				#if ort=="Choose Orientation Field":
					self.file_tree_full[i][-2][2]= 0
				#else:
				#	self.file_tree_full[i][-2][2]= ort

				if img=="Choose Image Field":
					self.file_tree_full[i][-2][3]= 0
				else:
					self.file_tree_full[i][-2][3]= img
				self.file_tree_full[i][1] ='Complete'
		self.insert_to_tree(self.file_tree_full)
		self.lat_field.config(width=20,fg='chartreuse4')
		self.lng_field.config(width=20,fg='chartreuse4')

	def clear(self):
		self.file_tree_full =[]
		self.output_dir_entry.destroy()
		self.output_dir_entry=Entry(self.footer_frame,width=60)
		self.output_dir_entry.grid(row=0,column=1,pady=20)
		x = self.file_listbox.get_children()
		for u in x:
			self.file_listbox.delete(u)
		self.lat_label.set('Choose Latitude Field')
		self.lng_label.set('Choose Longitude Field')
		self.image_label.set('Choose Image Field')

		self.lat_field.grid_forget()
		self.lng_field.grid_forget()
		self.image_field.grid_forget()

		self.lat_field = OptionMenu(self.content_left_frame,self.lat_label,*self.list_headers)
		self.image_field = OptionMenu(self.content_right_frame,self.image_label,*self.list_headers)
		self.lng_field = OptionMenu(self.content_left_frame,self.lng_label,*self.list_headers)

		self.lat_field.config(width=20)
		self.lng_field.config(width=20)
		self.image_field.config(width=20)

		self.lat_field.grid(row=2,column=0,sticky=W+E)
		self.lng_field.grid(row=3,column=0,sticky=W+E)
		self.image_field.grid(row=0,column=0,sticky=N+S)
		self.kmlvar.set(0)
		self.shapevar.set(0)
		self.downloadvar.set(0)
		self.pb["value"]= 0

	def validate(self):
		error=[]
		if not self.file_tree_full:
			 error.append('*Not Files added (Step1)')
		else:
			for i in self.file_tree_full:
				if i[1] =='Incomplete':
					error.append('*File(s) Incomplete ')
					break

		outputdir = self.output_dir_entry.get()
		kmz = self.kmlvar.get()
		shape = self.shapevar.get()
		download = self.downloadvar.get()

		if (kmz == 0) & (shape == 0) & (download ==0):
			error.append('*No Exports Selected')

		for i in range(len(self.file_tree_full)):
			if self.file_tree_full[i][-2][3] != 0:
				image_check = True
				break
			else:
				image_check = False

		if (image_check ==False) & (download==1):
			error.append('No Image Field Selected')

		if outputdir =='':
			error.append('*Output Incomplete  ')
		return error
	def run(self):
		errors = self.validate()
		if not errors:
			self.pb.start()
			self.proc_count = 0
			def onExit():
				proc_len = len(parm)
				#value = value+(100/len(self.file_tree_full))
				if self.proc_count == proc_len:
					self.pb.stop()
					self.pb["value"]= 100
					try:
						os.startfile(self.output_dir_entry.get())
					except:
						print 'cant open'

			def shapeThread(*popenArgs):
				proc = create_shape(*popenArgs)
				self.proc_count = self.proc_count+1
				onExit()
			def kmzThread(*popenArgs):
				proc = kmz_main(*popenArgs)
				self.proc_count = self.proc_count+1
				onExit()
			def imageThread(*popenArgs):
				proc = download_images(*popenArgs)
				self.proc_count = self.proc_count+1
				onExit()
			
			#self.run_button.destroy()
			#self.run_button = Button(self.footer_button_frames,text="Run", command=self.run,width=15)
			#self.run_button.grid(row=0,column=2,padx=10)

			value = 0
			self.message_lable.destroy()
			self.message_lable = Label(self.select_frame_right,text='Processing Status:',width=35)
			self.message_lable.grid(row=0,column=0,sticky=E)
			kmz = self.kmlvar.get()
			shape = self.shapevar.get()
			img = self.downloadvar.get()
			out_put= self.output_dir_entry.get()+'/'

			parm = []
			for f in range(len(self.file_tree_full)):
				new_dir = out_put+self.file_tree_full[f][0].replace('.csv','')
				#print new_dir
				if not os.path.exists(new_dir):
					os.makedirs(new_dir)
			#proc = subprocess.Popen(['python','args+test.py'],stdout=subprocess.PIPE)
				
				if (kmz == 1):
					parm.append(1)
					pa = [new_dir,str(self.file_tree_full[f][2]),str(self.file_tree_full[f][-2][0]),str(self.file_tree_full[f][-2][1]),str(self.file_tree_full[f][0])]
					thread = threading.Thread(target=kmzThread, args=pa)
					thread.start()
				if(shape == 1):
					parm.append(1)
					pa = [str(self.file_tree_full[f][0]),str(self.file_tree_full[f][-2][0]),str(self.file_tree_full[f][-2][1]),new_dir,str(self.file_tree_full[f][2])]
					thread = threading.Thread(target=shapeThread, args=pa)
					thread.start()
				if (img == 1):
					if self.file_tree_full[f][-2][-1] !=0:
						if not os.path.exists(new_dir+'/image'):
							os.makedirs(new_dir+'/image')
						parm.append(1)
						pai = [self.file_tree_full[f][2],self.file_tree_full[f][-2][-1],new_dir+'/image']
						thread = threading.Thread(target=imageThread, args=pai)
						thread.start()
						#parm.append(['python','src/image_download.py',self.file_tree_full[f][2],self.file_tree_full[f][-2][-1],new_dir+'/image'])
						#proc_image = subprocess.Popen(['python','image_download.py',self.file_tree_full[f][2],self.file_tree_full[f][-2][-1],new_dir+'/image'])
				
			#for p in parm:
				#thread = threading.Thread(target=runInThread, args=p)
				#thread.start()

				#value = value+(100/len(self.file_tree_full))
				#self.pb["value"]= value

			#self.pb.stop()
			#self.pb["value"]= 100
			#while proc_image.returncode ==None:
			#	print proc_image.poll()
			#self.pb.stop
			#self.pb["value"]= 100


		else:
			error_message= '\n'.join(errors)
			self.message_lable.destroy()
			self.message_lable = Label(self.select_frame_right,text=error_message,fg='Red',width=35)
			self.message_lable.grid(row=0,column=0,sticky=E)



root = Tk()
app = MainFrame(root)
#background_image=PhotoImage(file="./P1050982.jpg")
#root.configure(background = 'red')
#root.geometry('700x700+500+500')
root.geometry('700x700')
root.title('GeoODK')
root.resizable(width=FALSE, height=TRUE)
try:
	#'icons\logo_64.ico'
	root.wm_iconbitmap('icons\logo_64.ico')
except:
	print 'No Icon Found'


root.mainloop()

