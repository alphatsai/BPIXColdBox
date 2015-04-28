#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from Tkinter import *

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini
from readConfg import elComandante_conf

BG_framTitle='Gray'
BG_framConfig='LightBlue1'
BG_framMain='DarkSlateGray1'

class interface():
	def __init__(self, master=None):
		self.master = master
		self.framTitle = Frame(master, bg=BG_framTitle)
		self.framConfig = Frame(master, bg=BG_framConfig, relief=RAISED, borderwidth=2)
		self.framMain = Frame(master, bg=BG_framMain, relief=RAISED, borderwidth=2)
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
	
	def createWidgets(self):

		self.framTitle.grid(row=0, column=0)
		self.title = Label(self.framTitle, bg=BG_framTitle)	
		self.title["text"]="elComandante_ini"
		self.title.grid(row=0, column=0, columnspan=1 )

		self.framConfig.grid(row=1, column=0)
		self.lableConfig = Label(self.framConfig, bg=BG_framConfig)
		self.lableConfig["text"]="Configure input"	
		self.lableConfig.grid(row=0, column=0, sticky=E)

		self.entryConfig = Entry(self.framConfig)
		self.entryConfig["width"]=10	
		self.entryConfig.insert(0, self.loadConfig)	
		self.entryConfig.grid(row=0, column=1)
		
		self.button1Config = Button(self.framConfig, bg="IndianRed2")
		self.button1Config["text"]="ReLoad"
		self.button1Config.grid(row=0, column=2)
	
		self.button2Config = Button(self.framConfig, bg="SpringGreen2")
		self.button2Config["text"]="Save"
		self.button2Config.grid(row=0, column=3)

		self.framMain.grid(row=2, column=0)
		self.title1Main = Label(self.framMain, bg=BG_framMain)
		self.title1Main['text']='DTB setting'
		self.title1Main.grid(row=0, column=0, columnspan=1)

	def loadConfig(self, config=""):
		self.iniClass = elComandante_ini()
		self.iniClass.getDefault(config)
		self.nSections = len(self.iniClass.list_Sections)-len(self.iniSkipLists)
		self.loadConfig = config	

####### example ########
if __name__ == '__main__':
	root = Tk()
	#root.geometry("400x400+300+300") 
	app = interface(master=root)
	app.loadConfig("./elComandante.ini.default")
	app.createWidgets()
	root.mainloop()
