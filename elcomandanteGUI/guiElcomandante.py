#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from Tkinter import *
import tkFont

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini
from readConfg import elComandante_conf

BG_framTitle='Gray'
BG_framConfig='LightBlue1'
BG_framMain='wheat1'

class interface():
	def __init__(self, master=None):
		self.master = master
		self.master.title("guiElcomandante")
		self.master["bg"]=BG_framMain
		self.framMain =  self.master
		#self.framMain = Frame(self.master, bg=BG_framMain, relief=RAISED, borderwidth=2)
		#self.framMain = Frame(self.master, relief=RAISED, borderwidth=2)
		self.framMain.grid()
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

		self.title = Label(self.framMain, bg=BG_framMain, font=('helvetica', 10, 'bold') )
		self.title["text"]="elComandante_ini"
		self.title.grid(row=0, column=0, columnspan=6, sticky=NSEW )
		#self.title.pack(fill=X, side=TOP)

		col=0
		colmax=6
		while ( col < colmax ):
			self.pad = Label(self.framMain, bg=BG_framMain, width=10, height=2)
			self.pad.grid(row=1, column=col)
			col+=1

		# Config 
		self.lableConfig = Label(self.framMain, bg=BG_framMain, font=('helvetica', 12,))
		self.lableConfig["text"]="Input Configure"
		self.lableConfig.grid(row=1, column=0, columnspan=2)

		self.entryConfig = Entry(self.framMain)
		self.entryConfig["width"]=30
		self.entryConfig.insert(0, self.loadConfig)
		self.entryConfig.grid(row=1, column=2, sticky=W, columnspan=2)
		
		self.button1Config = Button(self.framMain, bg="IndianRed2", font=('helvetica', 12, 'bold'))
		self.button1Config["text"]="ReLoad"
		self.button1Config.grid(row=1, column=4, sticky=E)
	
		self.button2Config = Button(self.framMain, bg="SpringGreen2", font=('helvetica', 12,'bold'))
		self.button2Config["text"]="Save"
		self.button2Config.grid(row=1, column=5)
		
		# DTB = ['Modules', 'ModuleType', 'TestboardUse']
		self.title1Main = Label(self.framMain, bg=BG_framMain, font=('helvetica', 12,'bold'))
		self.title1Main['text']='DTB setting'
		self.title1Main.grid(row=2, column=0, columnspan=6, sticky=NSEW )
		
		self.modules = Frame(self.framMain, bg=BG_framMain)
		self.modules.grid(row=3, column=0, columnspan=2, sticky=N+E)
		self.modulesTitle = Label(self.modules, bg=BG_framMain, text='Modules', font=('helvetica', 12))
		self.modulesTitle.grid(row=0, column=0, columnspan=2)
		irow=1
		for opt in self.iniClass.list_Default['Modules']:
			newOptLabel = Label(self.modules, bg=BG_framMain)
			newOptEntry = Entry(self.modules)
			newOptLabel["text"] = opt
			newOptLabel.grid( row=irow, column=0, sticky=E+N )
			newOptEntry['width'] = 10
			newOptEntry.insert(0, self.iniClass.Sections['Modules'][opt])
			newOptEntry.grid( row=irow, column=1, sticky=W+N)
			irow+=1


		self.moduleType = Frame(self.framMain, bg=BG_framMain)
		self.moduleType.grid(row=3, column=2, columnspan=2, sticky=N)
		self.moduleTypeTitle = Label(self.moduleType, bg=BG_framMain, text='ModuleType', font=('helvetica', 12))
		self.moduleTypeTitle.grid(row=0, column=0, columnspan=2)
		irow=1
		for opt in self.iniClass.list_Default['ModuleType']:
			newOptLabel = Label(self.moduleType, bg=BG_framMain)
			var=StringVar()
			newOptMenu = OptionMenu(self.moduleType, var, "Full", "Roc" )
			newOptLabel["text"] = opt
			newOptLabel.grid( row=irow, column=0, sticky=E+N )
			newOptMenu['width'] =5 
			newOptMenu['bg'] = 'DeepPink2' 
			value=self.iniClass.Sections['ModuleType'][opt]
			if value !=  "Full" and value != "Roc":
				print ">> [ERROR] ModuleType "+opt+" has wrong value "+value
				var.set("Error")
			elif value=="Full":
				newOptMenu['bg'] = 'SkyBlue1' 
				var.set(value)
			elif value=="Roc":
				newOptMenu['bg'] = 'DarkOliveGreen1' 
				var.set(value)

			newOptMenu.grid( row=irow, column=1, sticky=W+N)
			irow+=1

		self.TestboardUse = Frame(self.framMain, bg=BG_framMain)
		self.TestboardUse.grid(row=3, column=4, columnspan=2, sticky=N+W)
		self.TestboardUseTitle = Label(self.TestboardUse, bg=BG_framMain, text='TestboardUse', font=('helvetica', 12))
		self.TestboardUseTitle.grid(row=0, column=0, columnspan=2)
		irow=1
		for opt in self.iniClass.list_Default['TestboardUse']:
			newOptLabel = Label(self.TestboardUse, bg=BG_framMain)
			newOptButton = Button(self.TestboardUse)
			newOptLabel["text"] = opt
			newOptLabel.grid( row=irow, column=0, sticky=E+N )
			newOptButton['width'] =5 
			value=self.iniClass.Sections['TestboardUse'][opt]
			newOptButton['text']="False"
			newOptButton['bg']="DarkOrange3"
			if value !=  "True" and value != "False":
				print ">> [ERROR] TestboardUse "+opt+" has wrong value "+value
			elif value == "True":
				newOptButton['text']=value
				newOptButton['bg']="green2"
			newOptButton.grid( row=irow, column=1, sticky=W+N)
			irow+=1

		# Hardware Setting = ['CoolingBox', 'Keithley', 'LowVoltage', 'Xray']
		self.title2Main = Label(self.framMain, bg=BG_framMain, font=('helvetica', 12,'bold'))
		self.title2Main['text']='Hardware setting'
		self.title2Main.grid(row=4, column=0, columnspan=6, sticky=NSEW )


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
