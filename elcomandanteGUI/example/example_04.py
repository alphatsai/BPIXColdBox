#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from Tkinter import *

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini 
from readConfg import elComandante_conf

class interface():
	def __init__(self, master=None):
		self.f0 = Frame(master, bg='black')
		self.f0.grid()
		self.iniClass = None
		self.nSections = 0
		self.iniSectionsLabel=[]
		self.iniOptionsLabel={}
		self.iniOptionsEntry={}
		self.iniSkipLists = [
			'Xray',
			'Environment Xrf',
			'Environment Mo',
			'Environment Ag',
			'Environment Ba',
			'Analysis VcalCalibrationStepAnalysisMo',
			'Analysis VcalCalibrationStepAnalysisAg',
			'Analysis VcalCalibrationStepAnalysisBa',
			'Analysis VcalVsThresholdAnalysis',
			'Analysis VcalCalibrationAnalysis'		
		]	
	
	def creatCanvas(self):
		f2 = Frame(self.f0, bg='black')
		f2.grid(row=0,column=0) 
		canvas = Canvas(f2, width=200, height=400, bg='white')  
		canvas.pack()                  
		canvas.create_line(0, 0, 200, 400) 

	def createWidgets(self):
		f1 = Frame(self.f0)
		f1.grid(row=1,column=0)	

		if self.iniClass == None:
			self.iniClass = elComandante_ini()

		colN=0
		sqrt = math.sqrt(self.nSections)
		if sqrt*10%10 == 0:
			colN=int(sqrt)
		else:
			colN=int(sqrt)+1
				
		sRow=0
		sCol=0
		isec=0
		for section in self.iniClass.list_Sections:
			if section in self.iniSkipLists:
				continue	
			fsub = Frame(f1)
			fsub.grid(row=sRow, column=sCol )
			newLable = Label(fsub)
			self.iniSectionsLabel.append(newLable)
			self.iniSectionsLabel[isec]['text']=section
			self.iniSectionsLabel[isec].grid(row=0, column=0, columnspan=2)
			self.iniOptionsLabel[section]=[]
			self.iniOptionsEntry[section]=[]
			sCol+=1
			if sCol > colN: 
				sCol=0
				sRow+=1
	
			irow=1
			iopt=0
			for opt in self.iniClass.list_Default[section]:
				newOptLabel = Label(fsub)
				newOptEntry = Entry(fsub)
				self.iniOptionsLabel[section].append(newOptLabel)
				self.iniOptionsLabel[section][iopt]["text"] = opt
				self.iniOptionsLabel[section][iopt].grid( row=irow, column=0 )
				self.iniOptionsEntry[section].append(newOptEntry)
				self.iniOptionsEntry[section][iopt]['width'] = 10
				self.iniOptionsEntry[section][iopt].insert(0, self.iniClass.Sections[section][opt])
				self.iniOptionsEntry[section][iopt].grid( row=irow, column=1)
				iopt+=1
				irow+=1
			isec+=1

	def loadConfig(self, config=""):
		self.iniClass = elComandante_ini()
		self.iniClass.getDefault(config)
		self.nSections = len(self.iniClass.list_Sections)-len(self.iniSkipLists)	

####### example ########
if __name__ == '__main__':
	root = Tk()
	#root.geometry("400x400+300+300") 
	app = interface(master=root)
	app.loadConfig("../elComandante.ini.default")
	app.creatCanvas()
	app.createWidgets()
	root.mainloop()
