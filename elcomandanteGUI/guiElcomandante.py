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
		self.framMain.grid()
		self.iniClass = None
		self.nSections = 0
		self.Labels={}
		self.Entries={}
		self.BoolButtons={}
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

	def loadConfig(self, config=""):
		self.iniClass = elComandante_ini()
		self.iniClass.getDefault(config)
		self.nSections = len(self.iniClass.list_Sections)-len(self.iniSkipLists)
		self.loadConfig = config	
		return

	def addQUIT(self, frame, row=0, column=0, text="QUIT", bg="IndianRed2", font=('helvetica', 12, 'bold'), columnspan=1, sticky='se'):
		self.QUIT = Button(frame, font=font, bg=bg, text=text, command=self.quit)
		self.QUIT.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)
		return

	def quit(self):
		print '>> [INFO] Ciao~ :-D'
		self.framMain.quit()
		return

	def addPreview(self, frame, row=0, column=0, text="Preview", bg="DeepSkyBlue2", font=('helvetica', 12, 'bold'), columnspan=1, sticky='se'):
		self.PREVIEW = Button(frame, font=font, bg=bg, text=text, command=self.printConfig)
		self.PREVIEW.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

	def printConfig(self):
		self.iniClass.callConfig()
		

	def addLabel(self, frame, label="", name0="", name1="", row=0, column=0, sticky='nsew', columnspan=1, bg=BG_framMain, font=("Arial",10)):
		newLabel = Label(frame, bg=bg, font=font)
		newLabel["text"] = name1
		newLabel.grid( row=row, column=column, sticky=sticky, columnspan=columnspan )
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		self.Labels[term1+term2+name1]=newLabel
		return

	def addEntry(self, frame, label="", name0="", name1="", value="" , row=0, column=0, width=10, sticky='nsew', columnspan=1 ):
		newEntry = Entry(frame)
		newEntry['width'] = width
		newEntry['bg']='white smoke'
		newEntry.insert(0, value)
		newEntry.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		self.Entries[term1+term2+name1]=newEntry
		return

	def addBoolButton(self, frame, label="", name0="", name1="", row=0, column=0, value='', sticky='wn', width=5):
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		name=term1+term2+name1

		newButton = Button(frame)
		newButton['width'] =width
		newButton['text']="False"
		newButton['bg']="DarkOrange3"
		newButton['command']=lambda:self.changeBool( name, name0, name1 )
		if value.lower() !=  "true" and value.lower() != "false":
			print ">> [ERROR] "+label+" '"+name+"' has wrong value '"+value+"'"
			print ">>         Please click the button to fix it" 
			newButton['text']='ERROR'
			newButton['bg']='DeepPink2'
		elif value == "True":
			newButton['text']="True"
			newButton['bg']="green2"
		newButton.grid( row=row, column=column, sticky=sticky)
		self.BoolButtons[name]=newButton
		return
	
	def changeBool(self, name, selction, option):
		if self.BoolButtons[name]['text'] == "False":
			print ">> [INFO] Change %s : %s : False -> True "%(selction, option)
			self.BoolButtons[name]['text']="True"
			self.BoolButtons[name]['bg']="green2"
			self.iniClass.changeOptValue(selction,option,"True")
		else:
			print ">> [INFO] Change %s : %s : %s -> False "%(selction, option, self.BoolButtons[name]['text'] )
			self.BoolButtons[name]['text']="False"
			self.BoolButtons[name]['bg']="DarkOrange3"
			self.iniClass.changeOptValue(selction,option,"False")
		return

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
		self.labelConfig = Label(self.framMain, bg=BG_framMain, font=('helvetica', 12,))
		self.labelConfig["text"]="Input Configure"
		self.labelConfig.grid(row=1, column=0, columnspan=2)

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
		self.addLabel( label='Main', name1='DTB', frame=self.framMain, row=2, column=0, columnspan=6, font=('helvetica', 12,'bold'), sticky='s' )
		
		self.modules = Frame(self.framMain, bg=BG_framMain)
		self.modules.grid(row=3, column=0, columnspan=2, sticky=N+E)
		self.addLabel( label='Main_DTB', name1='Modules', frame=self.modules, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['Modules']:
			value=self.iniClass.Sections['Modules'][opt]
			self.addLabel(label='Main_DTB', name0='Modules', name1=opt, frame=self.modules, row=irow, column=0 )
			self.addEntry(label='Main_DTB', name0='Modules', name1=opt, frame=self.modules, value=value, row=irow, column=1, width=10)
			irow+=1


		self.moduleType = Frame(self.framMain, bg=BG_framMain)
		self.moduleType.grid(row=3, column=2, columnspan=2, sticky=N)
		self.addLabel( label='Main_DTB', name1='ModuleType', frame=self.moduleType, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['ModuleType']:
			self.addLabel(label='Main_DTB', name0='ModuleType', name1=opt, frame=self.modules, row=irow, column=0 )
			var=StringVar()
			newOptMenu = OptionMenu(self.moduleType, var, "Full", "Roc" )
			newOptMenu['width'] =6
			newOptMenu['bg'] = 'DeepPink2'
			value=self.iniClass.Sections['ModuleType'][opt]
			if value !=  "Full" and value != "Roc":
				print ">> [ERROR] ModuleType "+opt+" has wrong value "+value
				var.set("ERROR")
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
		self.addLabel( label='Main_DTB', name1='TestboardUse', frame=self.TestboardUse, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['TestboardUse']:
			self.addLabel(label='Main_DTB', name0='TestboardUse', name1=opt, frame=self.modules, row=irow, column=0 )
			value=self.iniClass.Sections['TestboardUse'][opt]
			self.addBoolButton(label='Main_DTB', name0='TestboardUse', name1=opt, frame=self.TestboardUse, row=irow, column=1, value=value )
			irow+=1

		# Hardware Setting = ['CoolingBox', 'Keithley', 'LowVoltage', 'Xray']
		self.addLabel(label='Main', name1='Setup', frame=self.framMain, row=4, column=0, columnspan=6, font=('helvetica', 12,'bold'),sticky='s')

		self.CoolingBox = Frame(self.framMain, bg=BG_framMain)
		self.CoolingBox.grid(row=5, column=1, columnspan=1, sticky=N)
		self.addLabel( label='Main_Setup', name1='CoolingBox', frame=self.CoolingBox, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['CoolingBox']:
			self.addLabel(label='Main_Setup', name0='CoolingBox', name1=opt, frame=self.CoolingBox, row=irow, column=0 )
			irow+=1
			value=self.iniClass.Sections['CoolingBox'][opt]
			if opt == 'CoolingBoxUse':
				self.addBoolButton(label='Main_Setup', name0='CoolingBox', name1=opt, frame=self.CoolingBox, row=irow, column=0, value=value, sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='CoolingBox', name1=opt, frame=self.CoolingBox, value=value, row=irow, column=0, width=10)
			irow+=1

		self.Keithley = Frame(self.framMain, bg=BG_framMain)
		self.Keithley.grid(row=5, column=2, columnspan=1, sticky=N)
		self.addLabel( label='Main_Setup', name1='Keithley', frame=self.Keithley, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['Keithley']:
			self.addLabel(label='Main_Setup', name0='Keithley', name1=opt, frame=self.Keithley, row=irow, column=0 )
			irow+=1
			value=self.iniClass.Sections['Keithley'][opt]
			if opt == 'KeithleyUse':
				self.addBoolButton(label='Main_Setup', name0='Keithley', name1=opt, frame=self.Keithley, row=irow, column=0, value=value, sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='Keithley', name1=opt, frame=self.Keithley, value=value, row=irow, column=0, width=10)
			irow+=1

		self.LowVoltage = Frame(self.framMain, bg=BG_framMain)
		self.LowVoltage.grid(row=5, column=3, columnspan=1, sticky=N)
		self.addLabel( label='Main_Setup', name1='LowVoltage', frame=self.LowVoltage, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['LowVoltage']:
			self.addLabel(label='Main_Setup', name0='LowVoltage', name1=opt, frame=self.LowVoltage, row=irow, column=0 )
			irow+=1
			value=self.iniClass.Sections['LowVoltage'][opt]
			if opt == 'LowVoltageUse':
				self.addBoolButton(label='Main_Setup', name0='LowVoltage', name1=opt, frame=self.LowVoltage, row=irow, column=0, value=value, sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='LowVoltage', name1=opt, frame=self.LowVoltage, value=value, row=irow, column=0, width=10)
			irow+=1

		self.Xray = Frame(self.framMain, bg=BG_framMain)
		self.Xray.grid(row=5, column=4, columnspan=1, sticky=N)
		self.addLabel( label='Main_Setup', name1='Xray', frame=self.Xray, row=0, column=0, columnspan=2, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['Xray']:
			self.addLabel(label='Main_Setup', name0='Xray', name1=opt, frame=self.Xray, row=irow, column=0 )
			irow+=1
			value=self.iniClass.Sections['Xray'][opt]
			if opt == 'XrayUse':
				self.addBoolButton(label='Main_Setup', name0='Xray', name1=opt, frame=self.Xray, row=irow, column=0, value=value, sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='Xray', name1=opt, frame=self.Xray, value=value, row=irow, column=0, width=10)
			irow+=1

		# Process = ['Test Trim', 'Tests', 'OperationDetails']
		self.addLabel(label='Main', name1='Process',frame=self.framMain, row=6, column=0, columnspan=6, font=('helvetica', 12,'bold'),sticky='s')
	
		# Options 
		self.addPreview( self.framMain, row=7, column=4)
		self.addQUIT( self.framMain, row=7, column=5 )
		return

####### example ########
if __name__ == '__main__':
	root = Tk()
	#root.geometry("400x400+300+300") 
	app = interface(master=root)
	app.loadConfig("./elComandante.ini.default")
	app.createWidgets()
	root.mainloop()
