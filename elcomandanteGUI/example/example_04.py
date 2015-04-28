#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from Tkinter import *

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini
from readConfg import elComandante_conf

class interface():
	def __init__(self, master=None):
		self.f0 = Frame(master, bg='Gray')
		self.f0.grid()
		self.f1 = None
		self.f2 = None
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
		fpad = Frame(self.f0, height=20, bd=1, relief=RAISED, bg='Gray', )
		self.f2 = Frame(self.f0, bg='black', height=200, relief=SUNKEN, borderwidth=3)
		if self.f1 != None:
			fpad.grid(row=2, column=0, )	
			self.f2.grid(row=3,column=0)
		else:	
			fpad.grid(row=0, column=0, )	
			self.f2.grid(row=1,column=0)

		canvas = Canvas(self.f2, width=600, height=200, bg='White')
		canvas.pack()
		canvas.create_line(0, 0, 600, 200)

	def createWidgets(self):
		fpad = Frame(self.f0, height=20, bd=1,  bg='Gray', )
		self.f1 = Frame(self.f0, relief=RAISED, borderwidth=2)
		if self.f2 != None:
			fpad.grid(row=2, column=0, )	
			self.f1.grid(row=3,column=0)
		else:
			fpad.grid(row=0, column=0, )	
			self.f1.grid(row=1,column=0)

		if self.iniClass == None:
			self.iniClass = elComandante_ini()

		colN=0
		sqrt = math.sqrt(self.nSections)
		if sqrt*10%10 == 0:
			colN=int(sqrt)+2
		else:
			colN=int(sqrt)+1+2

		sRow=0
		sCol=0
		isec=0
		for section in self.iniClass.list_Sections:
			if section in self.iniSkipLists:
				continue
			fsub = Frame(self.f1)
			if sCol == 0:
				fspad = Frame(self.f1, width=10)
				fspad.grid(row=sRow, column=sCol, sticky=N )
				sCol+=1
				fsub.grid(row=sRow, column=sCol, sticky=N )
			else:		
				fsub.grid(row=sRow, column=sCol, sticky=N )

			newLable = Label(fsub)
			self.iniSectionsLabel.append(newLable)
			self.iniSectionsLabel[isec]['text']=section
			self.iniSectionsLabel[isec].grid(row=0, column=0, columnspan=2, sticky=N)
			self.iniOptionsLabel[section]=[]
			self.iniOptionsEntry[section]=[]
	
			irow=1
			iopt=0
			for opt in self.iniClass.list_Default[section]:
				newOptLabel = Label(fsub)
				newOptEntry = Entry(fsub)
				self.iniOptionsLabel[section].append(newOptLabel)
				self.iniOptionsLabel[section][iopt]["text"] = opt
				self.iniOptionsLabel[section][iopt].grid( row=irow, column=0, sticky=E+N )
				self.iniOptionsEntry[section].append(newOptEntry)
				self.iniOptionsEntry[section][iopt]['width'] = 10
				self.iniOptionsEntry[section][iopt].insert(0, self.iniClass.Sections[section][opt])
				self.iniOptionsEntry[section][iopt].grid( row=irow, column=1, sticky=W+N)
				iopt+=1
				irow+=1
			isec+=1
			sCol+=1

			if sCol == colN-1 or section == self.iniClass.list_Sections[len(self.iniClass.list_Sections)-1]: 
				fspad = Frame(self.f1, width=10)
				fspad.grid(row=sRow, column=sCol, sticky=N )
				sCol=0
				sRow+=1
				fspad = Frame(self.f1, height=20)
				fspad.grid(row=sRow, column=sCol, sticky=N, columnspan=colN)
				sRow+=1

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
