#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from Tkinter import *
import tkFont

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini
from readConfg import elComandante_conf

COLUMNMAX=9
BG_framTitle='Gray'
BG_framConfig='LightBlue1'
BG_framMain='wheat1'
TRUE_COLOR='OliveDrab1'
FALSE_COLOR='PeachPuff3'
ERROR_COLOR='DeepPink2'
PREVIEW_COLOR='CadetBlue2'
MENU_FULL_COLOR='SkyBlue1'
MENU_ROC_COLOR='MediumPurple1'

class interface():
	def __init__(self, master=None):
		self.master = master
		self.master.title("guiElcomandante")
		self.master["bg"]=BG_framMain
		self.master.grid()
		self.iniClass = None
		self.nSections = 0
		self.Labels={}
		self.Entries={}
		self.BoolButtons={}
		self.testButtons={}
		self.MuduelTypeMenu={}
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

	def addXpad(self, frame, colmax=8, bg=BG_framMain, width=10, height=1, row=0):
		col=0
		while ( col < colmax ):
			pad = Label(frame, bg=bg, width=width, height=height)
			pad.grid(row=row, column=col)
			col+=1
		return

	def addQUIT(self, frame, row=0, column=0, text="QUIT", bg="IndianRed2", font=('helvetica', 12, 'bold'), columnspan=1, sticky='se'):
		self.QUIT = Button(frame, font=font, bg=bg, text=text, command=self.quit)
		self.QUIT.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)
		return

	def quit(self):
		print '>> [INFO] Ciao~ :-D'
		self.master.quit()
		return

	def addPreview(self, frame, row=0, column=0, text="Preview", bg=PREVIEW_COLOR, font=('helvetica', 12, 'bold'), columnspan=1, sticky='se'):
		self.PREVIEW = Button(frame, font=font, bg=bg, text=text, command=self.printConfig)
		self.PREVIEW.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

	def printConfig(self):
		self.iniClass.callConfig()
		

	def addLabel(self, frame, label="", name0="", name1="", row=0, column=0, sticky='nsew', columnspan=1, rowspan=1, bg=BG_framMain, font=("Arial",10)):
		newLabel = Label(frame, bg=bg, font=font)
		newLabel["text"] = name1
		newLabel.grid( row=row, column=column, sticky=sticky, columnspan=columnspan, rowspan=rowspan )
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
		newButton['text']="OFF"
		newButton['bg']=FALSE_COLOR
		newButton['command']=lambda:self.changeBool( name, name0, name1 )
		if value.lower() !=  "true" and value.lower() != "false":
			print ">> [ERROR] "+name0+" '"+name1+"' has wrong value '"+value+"'"
			print ">>         Please click the button to fix it" 
			newButton['text']='ERROR'
			newButton['bg']=ERROR_COLOR
		elif value == "True":
			newButton['text']="ON"
			newButton['bg']=TRUE_COLOR
		newButton.grid( row=row, column=column, sticky=sticky)
		self.BoolButtons[name]=newButton
		return
	
	def changeBool(self, name, selction, option):
		if self.BoolButtons[name]['text'] == "OFF":
			print ">> [INFO] Change %s : %s : False -> True "%(selction, option)
			self.BoolButtons[name]['text']="ON"
			self.BoolButtons[name]['bg']=TRUE_COLOR
			self.iniClass.changeOptValue(selction,option,"True")
		else:
			print ">> [INFO] Change %s : %s : %s -> False "%(selction, option, self.BoolButtons[name]['text'] )
			self.BoolButtons[name]['text']="OFF"
			self.BoolButtons[name]['bg']=FALSE_COLOR
			self.iniClass.changeOptValue(selction,option,"False")
		return

	def addTestButton(self, frame, label="", name0="", name1="", row=0, column=0, sticky='n', width=10, rowspan=1):
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		name=term1+term2+name1

		newButton = Button(frame)
		newButton['width'] =width
		newButton['text']=name1
		newButton['bg']=FALSE_COLOR
		newButton.grid( row=row, column=column, sticky=sticky, rowspan=rowspan)
		self.testButtons[name]=newButton
		return

	def addMuduelTypeMenu(self, frame, label="", name0="", name1="", row=0, column=0, value='', sticky='wn', width=10):
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		name=term1+term2+name1

		var=StringVar()
		newMenu = OptionMenu( frame, var, () )
		newMenu['width'] = width
		newMenu['bg'] = ERROR_COLOR
		if value.lower() !=  "full" and value.lower() != "roc":
			print ">> [ERROR] "+label+" '"+name+"' has wrong value '"+value+"'"
			print ">>         Please select the type to fix it" 
			var.set("ERROR")
		elif value=="Full":
			newMenu['bg'] = MENU_FULL_COLOR
			var.set(value)
		elif value=="Roc":
			newMenu['bg'] = MENU_ROC_COLOR
			var.set(value)
		newMenu.grid( row=row, column=column, sticky=sticky)
		newMenu['menu'].delete(0)
		newMenu['menu'].add_command( label="Full", command=lambda:self.chooseFull(newMenu, name0, name1, var))
		newMenu['menu'].add_command( label="Roc",  command=lambda:self.chooseRoc(newMenu, name0, name1, var))
		self.MuduelTypeMenu[name]=newMenu

	def chooseFull(self, menu, selction, option, var):
		value = self.iniClass.Sections[selction][option]
		if value != 'Full':
			print ">> [INFO] Change %s : %s : %s -> Full "%(selction, option, value)
			menu['bg'] = MENU_FULL_COLOR
			var.set('Full')
			self.iniClass.changeOptValue(selction,option,"Full")
		return

	def chooseRoc(self, menu, selction, option, var):
		value = self.iniClass.Sections[selction][option]
		if value != 'Roc':
			print ">> [INFO] Change %s : %s : %s -> Roc "%(selction, option, value)
			menu['bg'] = MENU_ROC_COLOR
			var.set('Roc')
			self.iniClass.changeOptValue(selction,option,"Roc")
		return

	def createWidgets(self):
		# Title
		mainRow=0
		self.title = Label(self.master, bg=BG_framMain, font=('helvetica', 10, 'bold') )
		self.title["text"]="elComandante_ini"
		self.title.grid(row=mainRow, column=0, columnspan=COLUMNMAX, sticky=NSEW )

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		# Config 
		mainRow+=1
		self.addLabel(label='Main', name1='Input Configure', frame=self.master, row=mainRow, column=2, font=('helvetica', 12))

		self.entryConfig = Entry(self.master)
		self.entryConfig["width"]=35
		self.entryConfig.insert(0, self.loadConfig)
		self.entryConfig.grid(row=mainRow, column=3, columnspan=2 )
		
		self.button1Config = Button(self.master, bg="IndianRed2", font=('helvetica', 12, 'bold'))
		self.button1Config["text"]="ReLoad"
		self.button1Config.grid(row=mainRow, column=5, sticky=E)
	
		self.button2Config = Button(self.master, bg="SpringGreen2", font=('helvetica', 12,'bold'))
		self.button2Config["text"]="Save"
		self.button2Config.grid(row=mainRow, column=6)
		
		self.button2Config = Button(self.master, bg=PREVIEW_COLOR, font=('helvetica', 12,'bold'))
		self.button2Config["text"]="Next"
		self.button2Config.grid(row=mainRow, column=7, sticky='w')

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		# DTB = ['Modules', 'ModuleType', 'TestboardUse']
		mainRow+=1
		self.addLabel( label='Main', name1='DTB', frame=self.master, row=mainRow, columnspan=COLUMNMAX, font=('helvetica', 12,'bold'), sticky='s' )
	
		mainRow+=1
		self.options = Frame( self.master, bg=BG_framMain)
		self.tb0 = Frame( self.master, bg=BG_framMain)
		self.tb1 = Frame( self.master, bg=BG_framMain)
		self.tb2 = Frame( self.master, bg=BG_framMain)
		self.tb3 = Frame( self.master, bg=BG_framMain)
		self.options.grid( row=mainRow, column=1, sticky=S)
		self.tb0.grid( row=mainRow, column=2, sticky=N)
		self.tb1.grid( row=mainRow, column=3, sticky=N)
		self.tb2.grid( row=mainRow, column=4, sticky=N)
		self.tb3.grid( row=mainRow, column=5, sticky=N)

		self.addLabel( label='Main_DTB', name1='Modules', frame=self.options, row=1, font=('helvetica', 12,))
		self.addLabel( label='Main_DTB', name1='ModuleType', frame=self.options, row=2, font=('helvetica', 12,))
		self.addLabel( label='Main_DTB', name1='TestboardUse', frame=self.options, row=3, font=('helvetica', 12,))

		self.addLabel( label='Main_DTB', name1='TB0', frame=self.tb0, font=('helvetica', 12,))
		self.addLabel( label='Main_DTB', name1='TB1', frame=self.tb1, font=('helvetica', 12,))
		self.addLabel( label='Main_DTB', name1='TB2', frame=self.tb2, font=('helvetica', 12,))
		self.addLabel( label='Main_DTB', name1='TB3', frame=self.tb3, font=('helvetica', 12,))

		value0=self.iniClass.Sections['Modules']['TB0']
		value1=self.iniClass.Sections['Modules']['TB1']
		value2=self.iniClass.Sections['Modules']['TB2']
		value3=self.iniClass.Sections['Modules']['TB3']
		self.addEntry(label='Main_DTB', name0='Modules', name1='TB0', frame=self.tb0, value=value0, row=1)
		self.addEntry(label='Main_DTB', name0='Modules', name1='TB1', frame=self.tb1, value=value1, row=1)
		self.addEntry(label='Main_DTB', name0='Modules', name1='TB2', frame=self.tb2, value=value2, row=1)
		self.addEntry(label='Main_DTB', name0='Modules', name1='TB3', frame=self.tb3, value=value3, row=1)

		value0=self.iniClass.Sections['ModuleType']['TB0']
		value1=self.iniClass.Sections['ModuleType']['TB1']
		value2=self.iniClass.Sections['ModuleType']['TB2']
		value3=self.iniClass.Sections['ModuleType']['TB3']
		self.addMuduelTypeMenu( label='Main_DTB', name0='ModuleType', name1='TB0', frame=self.tb0, value=value0, row=2)
		self.addMuduelTypeMenu( label='Main_DTB', name0='ModuleType', name1='TB1', frame=self.tb1, value=value1, row=2)
		self.addMuduelTypeMenu( label='Main_DTB', name0='ModuleType', name1='TB2', frame=self.tb2, value=value2, row=2)
		self.addMuduelTypeMenu( label='Main_DTB', name0='ModuleType', name1='TB3', frame=self.tb3, value=value3, row=2)

		value0=self.iniClass.Sections['TestboardUse']['TB0']
		value1=self.iniClass.Sections['TestboardUse']['TB1']
		value2=self.iniClass.Sections['TestboardUse']['TB2']
		value3=self.iniClass.Sections['TestboardUse']['TB3']
		self.addBoolButton( label='Main_DTB', name0='TestboardUse', name1='TB0', frame=self.tb0, value=value0, row=3, sticky='we')
		self.addBoolButton( label='Main_DTB', name0='TestboardUse', name1='TB1', frame=self.tb1, value=value1, row=3, sticky='we')
		self.addBoolButton( label='Main_DTB', name0='TestboardUse', name1='TB2', frame=self.tb2, value=value2, row=3, sticky='we')
		self.addBoolButton( label='Main_DTB', name0='TestboardUse', name1='TB3', frame=self.tb3, value=value3, row=3, sticky='we')

		# Hardware Setting = ['CoolingBox', 'Keithley', 'LowVoltage', 'Xray']
		mainRow+=1
		self.addLabel(label='Main', name1='Setup', frame=self.master, row=mainRow, columnspan=COLUMNMAX, font=('helvetica', 12,'bold'),sticky='s')

		mainRow+=1
		self.CoolingBox = Frame( self.master, bg=BG_framMain)
		self.CoolingBox.grid( row=mainRow, column=2, sticky=N)
		self.addLabel( label='Main_Setup', name1='CoolingBox', frame=self.CoolingBox, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['CoolingBox']:
			self.addLabel(label='Main_Setup', name0='CoolingBox', name1=opt, frame=self.CoolingBox, row=irow )
			irow+=1
			value=self.iniClass.Sections['CoolingBox'][opt]
			if opt == 'CoolingBoxUse':
				self.addBoolButton(label='Main_Setup',name0='CoolingBox',name1=opt,frame=self.CoolingBox,row=irow,value=value,sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='CoolingBox', name1=opt, frame=self.CoolingBox, value=value, row=irow)
			irow+=1

		self.Keithley = Frame( self.master, bg=BG_framMain)
		self.Keithley.grid( row=mainRow, column=3, sticky=N)
		self.addLabel( label='Main_Setup', name1='Keithley', frame=self.Keithley, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['Keithley']:
			self.addLabel(label='Main_Setup', name0='Keithley', name1=opt, frame=self.Keithley, row=irow )
			irow+=1
			value=self.iniClass.Sections['Keithley'][opt]
			if opt == 'KeithleyUse':
				self.addBoolButton(label='Main_Setup', name0='Keithley', name1=opt, frame=self.Keithley, row=irow, value=value, sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='Keithley', name1=opt, frame=self.Keithley, value=value, row=irow)
			irow+=1

		self.LowVoltage = Frame( self.master, bg=BG_framMain)
		self.LowVoltage.grid( row=mainRow, column=4, sticky=N)
		self.addLabel( label='Main_Setup', name1='LowVoltage', frame=self.LowVoltage, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['LowVoltage']:
			self.addLabel(label='Main_Setup', name0='LowVoltage', name1=opt, frame=self.LowVoltage, row=irow )
			irow+=1
			value=self.iniClass.Sections['LowVoltage'][opt]
			if opt == 'LowVoltageUse':
				self.addBoolButton(label='Main_Setup',name0='LowVoltage',name1=opt,frame=self.LowVoltage,row=irow,value=value,sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='LowVoltage', name1=opt, frame=self.LowVoltage, value=value, row=irow)
			irow+=1

		self.Xray = Frame( self.master, bg=BG_framMain)
		self.Xray.grid( row=mainRow, column=5, sticky=N)
		self.addLabel( label='Main_Setup', name1='Xray', frame=self.Xray, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['Xray']:
			self.addLabel(label='Main_Setup', name0='Xray', name1=opt, frame=self.Xray, row=irow)
			irow+=1
			value=self.iniClass.Sections['Xray'][opt]
			if opt == 'XrayUse':
				self.addBoolButton(label='Main_Setup', name0='Xray', name1=opt, frame=self.Xray, row=irow, value=value, sticky='n')
			else:
				self.addEntry(label='Main_Setup', name0='Xray', name1=opt, frame=self.Xray, value=value, row=irow)
			irow+=1

		# Process = ['Tests', 'OperationDetails']
		mainRow+=1
		self.addLabel(label='Main', name1='Process',frame=self.master, row=mainRow, columnspan=COLUMNMAX, font=('helvetica', 12,'bold'),sticky='s')

		mainRow+=1
		self.Tests = Frame( self.master, bg=BG_framMain)
		self.Tests.grid( row=mainRow, column=1, sticky=W+N, columnspan=5 )
		#self.addLabel( label='Main_Process', name1='Tests', frame=self.Tests, columnspan=6, font=('helvetica', 12,))
		irow=1
		for opt in self.iniClass.list_Default['Tests']:
			self.addLabel(label='Main_Process', name0='Tests', name1=opt, frame=self.Tests, row=irow)
			value=self.iniClass.Sections['Tests'][opt]
			if opt == 'Test':
				self.addEntry(label='Main_Process', name0='Tests', name1=opt, frame=self.Tests, value=value, row=irow, column=1, width=20, columnspan=5)
				irow+=1
				self.addLabel(label='Main_Process', name0='Tests', name1='Options', frame=self.Tests, row=irow, rowspan=2, sticky='ns')
				self.addTestButton(label='Main_Process', name0='Tests', name1='IV@17', frame=self.Tests, row=irow, column=1, sticky='ne' )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Pretest@17', frame=self.Tests, row=irow, column=2 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Fulltest@17', frame=self.Tests, row=irow, column=3 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Add new test', frame=self.Tests,row=irow,column=4,sticky='wn' )
				irow+=1
				self.addTestButton(label='Main_Process', name0='Tests', name1='IV@-20', frame=self.Tests, row=irow, column=1 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Pretest@-20', frame=self.Tests, row=irow, column=2 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Fulltest@-20', frame=self.Tests, row=irow, column=3 )
				self.addEntry(label='Main_Process', name0='Tests', name1='New Test', frame=self.Tests, value='Ex: IV@10', row=irow, column=4 )
			elif opt == 'TestDescription':
				self.addEntry(label='Main_Process', name0='Tests', name1=opt, frame=self.Tests, value=value, row=irow, column=1, columnspan=3)
				self.addTestButton(label='Main_Process', name0='Tests', name1='Delete', frame=self.Tests, row=irow, column=4 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Clear', frame=self.Tests, row=irow, column=5 )
			else:
				self.addEntry(label='Main_Process', name0='Tests', name1=opt, frame=self.Tests, value=value, row=irow, column=1)
			irow+=1
	
		# Options 
		mainRow+=1
		self.addPreview( self.master, row=mainRow, column=COLUMNMAX-3)
		self.addQUIT( self.master, row=mainRow, column=COLUMNMAX-2, sticky='w' )

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)
		return

####### example ########
if __name__ == '__main__':
	root = Tk()
	app = interface(master=root)
	app.loadConfig("./elComandante.ini.default")
	app.createWidgets()
	root.mainloop()
