#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from Tkinter import *
import tkFont

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini
from readConfg import elComandante_conf

Delay_MAX=8 #sec
CYCLE_MAX=20
COLUMNMAX=9
TITLE2_FONT=('helvetica', 15, 'bold')
SECTION_FONT=('helvetica', 10, 'bold')
OPTION_FONT=('helvetica', 10 )
BUTTON_FONT=('helvetica', 9, 'bold' )
BUTTON2_FONT=('helvetica', 10, 'bold' )
TITLE_COLOR='gray37'
TITLE2_COLOR='gray27'
TITLE3_COLOR='gray27'
TITLE4_COLOR='gray17'
BG_framMain='gray93'
TRUE_COLOR='OliveDrab1'
FALSE_COLOR='PeachPuff3'
ERROR_COLOR='IndianRed2'
PREVIEW_COLOR='medium sea green'
UNLOCK_COLOR='DarkOrange1'
LOCK_COLOR='goldenrod1'
RELOAD_COLOR='IndianRed2'
SAVE_COLOR='goldenrod1'
QUIT_COLOR='IndianRed2'
MENU_FULL_COLOR='LightSteelBlue1'
MENU_ROC_COLOR='light slate blue'
BYTYPING_COLOR='khaki1'
ENTRY_COLOR='snow'
ENTRY_LOCKED_COLOR='light grey'

class interface():
	#### initial parameters
	def __init__(self, master=None):
		self.master = master
		self.master.title("guiElcomandante")
		self.master["bg"]=BG_framMain
		self.master.grid()
		self.isfixed=True
		self.iniClass = None
		self.output=None
		self.Labels={}
		self.Entries={}
		self.BoolButtons={}
		self.testButtons={}
		self.Menu={}
	
	#### Load configure file
	def loadConfig(self, config=""):
		self.iniClass = elComandante_ini()
		self.iniClass.getDefault(config)
		self.loadConfig = config	
		return

	### Add empty pad for designing 
	def addXpad(self, frame, colmax=8, bg=BG_framMain, width=10, height=1, row=0):
		col=0
		while ( col < colmax ):
			pad = Label(frame, bg=bg, width=width, height=height)
			pad.grid(row=row, column=col)
			col+=1
		return

	### Lock button
	def lock(self):
		if self.buttonLock['text'] == 'Unlock':
			self.isfixed=False
			self.buttonLock['text']='Lock'
			self.buttonLock['bg']=LOCK_COLOR
			self.locklabel['fg']=BG_framMain
			for entry in self.Entries:
				self.Entries[entry]['bg']=ENTRY_COLOR
		else:
			self.isfixed=True
			self.buttonLock['text']='Unlock'
			self.buttonLock['bg']=UNLOCK_COLOR
			self.locklabel['fg']='red'
			for entry in self.Entries:
				self.Entries[entry]['bg']=ENTRY_LOCKED_COLOR
	
	def approchButton(self):
		self.now = self.buttonLock['text']
		if self.now == 'Locked':
			self.buttonLock['text']='Unlock'
		elif self.now == 'Unlocked':
			self.buttonLock['text']='Lock'
		return

	### Quit button
	def addQUIT(self, frame, row=0, column=0, text="QUIT", bg=QUIT_COLOR, font=BUTTON2_FONT, columnspan=1, sticky='se', width=5):
		self.QUIT = Button(frame, font=font, bg=bg, width=width, text=text, command=self.quit, fg=TITLE4_COLOR)
		self.QUIT.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)
		return

	def quit(self):
		print '>> [INFO] Ciao~ :-D'
		self.master.quit()
		return

	### Preview button
	def addPreview(self, frame, row=0, column=0, text="Preview", bg=PREVIEW_COLOR, font=BUTTON2_FONT,columnspan=1, sticky='se', width=5):
		self.PREVIEW = Button(frame, font=font, bg=bg, text=text, width=width, command=self.printConfig, fg=TITLE4_COLOR)
		self.PREVIEW.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)
		return

	def printConfig(self):
		self.iniClass.callConfig()
		return

	### Save button
	def addSave(self, frame, row=0, column=0, text="Save", bg=SAVE_COLOR, font=BUTTON2_FONT, columnspan=1, sticky='se', width=5):
		self.SAVE = Button(frame, font=font, bg=bg, text=text, width=width, fg=TITLE4_COLOR, command= lambda:self.saveConfig(self.output) )
		self.SAVE.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

	def saveConfig(self, output=None):
		self.iniClass.makeConfig(output)
		return

	### Add commend label 
	def addLabel(self, frame, label="", name0="", name1="", row=0, column=0, sticky='nsew', columnspan=1, rowspan=1, bg=BG_framMain, font=OPTION_FONT, fg=TITLE3_COLOR):
		newLabel = Label(frame, bg=bg, font=font, fg=fg)
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

	### Add commend entry 
	def addEntry(self, frame, label="", name0="", name1="", value="" , row=0, column=0, width=10, sticky='nsew', columnspan=1, fg='black' ):
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		name=term1+term2+name1

		newEntry = Entry(frame)
		newEntry['width'] = width
		newEntry['fg'] = fg
		if self.isfixed:
			newEntry['bg']=ENTRY_LOCKED_COLOR
		else:
			newEntry['bg']=ENTRY_COLOR
		newEntry.insert(0, value)
		newEntry.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		self.Entries[name]=newEntry
		return name

	### Add entry for options from configure file 
	def addOptEntry(self, frame, label="", name0="", name1="", value="" , row=0, column=0, width=10, sticky='nsew', columnspan=1, isFixed=False ):
		name = self.addEntry(frame, label, name0, name1, value, row, column, width, sticky, columnspan)
		newEntry = self.Entries[name]
		if isFixed:
			newEntry.bind('<Key>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1], True))
			newEntry.bind('<Leave>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1]))
			newEntry.bind('<Return>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1], True))
			newEntry.bind('<FocusOut>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1]))
		else:
			newEntry.bind('<Key>', lambda event:self.chEntryBG(newEntry,self.iniClass.Sections[name0][name1] ))
			newEntry.bind('<Leave>', lambda event:self.checkChanging(newEntry, self.iniClass.Sections[name0][name1] ))
			newEntry.bind('<Return>', lambda event:self.ConfirmChangeOpt(newEntry, name0, name1 ))
			newEntry.bind('<FocusOut>', lambda event:self.checkChanging(newEntry, self.iniClass.Sections[name0][name1] ))
		self.Entries[name]=newEntry
		return

	def chEntryBG(self, entry, value, murmur=True):
		if self.isfixed:
			self.unTouchEntry(entry, value, murmur)
			return
		entry['bg']=BYTYPING_COLOR
		return

	def checkChanging(self, entry, value, murmur=False):
		if self.isfixed:
			self.unTouchEntry(entry, value, murmur)
			return
		if value == entry.get():
			entry['bg']=ENTRY_COLOR
		return

	def ConfirmChangeOpt(self, entry, section, option, murmur=True):
		value = self.iniClass.Sections[section][option]
		if self.isfixed:
			self.unTouchEntry(entry, value, murmur)
			return
		newvalue = entry.get()
		if value != newvalue:
			print ">> [INFO] Change %s : %s : %s -> %s "%(section, option, value, newvalue)
			self.iniClass.changeOptValue(section,option, newvalue)
		entry['bg']=ENTRY_COLOR
		return

	def unTouchEntry(self, entry, value, murmur=False ):
		if murmur:
			print '>> [INFO] The entry is locked!'
		entry.delete(0, END)
		entry.insert(0, value)
		return	

	### Add button for bool options from configure file 
	def addBoolButton(self, frame, label="", name0="", name1="", row=0, column=0, columnspan=1, value='', sticky='wn', width=5):
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
		newButton['fg']=TITLE4_COLOR
		newButton['font']=BUTTON_FONT
		newButton['command']=lambda:self.changeBool( name, name0, name1 )
		if value.lower() !=  "true" and value.lower() != "false":
			print ">> [ERROR] "+name0+" '"+name1+"' has wrong value '"+value+"'"
			print ">>         Please click the button to fix it" 
			newButton['text']='ERROR'
			newButton['bg']=ERROR_COLOR
		elif value == "True":
			newButton['text']="ON"
			newButton['bg']=TRUE_COLOR
		newButton.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		self.BoolButtons[name]=newButton
	
	def changeBool(self, name, selction, option):
		if self.isfixed:
			print '>> [INFO] The button is locked!'
			return
			
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

	### Add button for Tests options from configure file 
	def addTestButton(self, frame, label="", name0="", name1="", row=0, column=0, sticky='n', width=10, rowspan=1, columnspan=1):
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		name=term1+term2+name1

		newButton = Button(frame, command=lambda:self.addTest(newButton))
		newButton['width'] =width
		newButton['text']=name1
		newButton['bg']=FALSE_COLOR
		newButton['fg']=TITLE4_COLOR
		newButton['font']=BUTTON_FONT
		newButton.grid( row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan)
		newButton.bind('<Button-1>', lambda event:self.changeColorTestEntry(0))
		newButton.bind('<Leave>', lambda event:self.changeColorTestEntry(1))
		self.testButtons[name]=newButton
		return

	def addTest(self, button):
		if self.isfixed:
			print '>> [INFO] The button is locked!'
			return

		if button['text'] == 'Clear':
			self.Entries['Main_Process_Tests_Test'].delete(0,END)
			self.iniClass.changeOptValue('Tests','Test', '')
			print ">> [INFO] Clear Tests! "
			print ">>        Changed Tests : "
			return

		tests = self.Entries['Main_Process_Tests_Test'].get()
		if button['text'] == 'Delete':
			restTests = ''
			if tests != '':
				lTests = tests.split(',')
				nTests = len(lTests)-1
				delTest = lTests[nTests]
				i = 0
				while ( i < nTests ):
					if i == nTests-1:
						restTests += lTests[i]
					else:
						restTests += lTests[i]+','
					i+=1
			else:
				return
			self.Entries['Main_Process_Tests_Test'].delete(0,END)
			self.Entries['Main_Process_Tests_Test'].insert(0, restTests)
			self.iniClass.changeOptValue('Tests','Test', restTests)
			print ">> [INFO] Delete a test '%s'"%(delTest)
			print ">>        Changed Tests %s: "%(restTests)
			return

		newprocess = button['text']
		if tests ==  '':
			tests=newprocess
		else:
			tests+=','+newprocess

		self.Entries['Main_Process_Tests_Test'].delete(0,END)
		self.Entries['Main_Process_Tests_Test'].insert(0, tests)
		self.iniClass.changeOptValue('Tests','Test', tests)
		print ">> [INFO] Add new process %s "%(newprocess)
		print ">>        Changed Tests : %s "%(tests)
		return

	def changeColorTestEntry(self, action):
		if self.isfixed:
			return

		if action == 0: #<Button-1>
			self.Entries['Main_Process_Tests_Test']['bg']=BYTYPING_COLOR
		elif action == 1: #<Leave>
			self.Entries['Main_Process_Tests_Test']['bg']=ENTRY_COLOR
		

	### Add Menu for delay measument IV from configure file 
	def addDelayMenu(self, frame, label="", name0="", name1="", row=0, column=0, value='', nmax=Delay_MAX, sticky='wn', width=10):
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
		newMenu['fg']=TITLE4_COLOR
		newMenu['font']=BUTTON_FONT
		if not value.isdigit():
			print ">> [ERROR] "+label+" '"+name+"' has wrong value '"+value+"'"
			print ">>         Please select the number to fix it" 
			var.set("ERROR")
		else:
			newMenu['bg'] = MENU_FULL_COLOR
			var.set(str(int(float(value)*2))+' Sec.')
		newMenu.grid( row=row, column=column, sticky=sticky)
		newMenu['menu'].delete(0)
		sec=1.
		while ( sec <= nmax ):
			newMenu['menu'].add_command(label=str(int(sec))+' Sec.',command=lambda sec=sec:self.chooseDelay( newMenu, sec, name0, name1, var))
			sec+=1
		self.Menu[name]=newMenu

	def chooseDelay(self, menu, sec, selction, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return

		value = self.iniClass.Sections[selction][option]
		if float(value)*2 != sec:
			print ">> [INFO] Change %s : %s : %s(%2.0f sec) -> %s(%2.0f sec) "%(selction, option, value, float(value)*2, str(sec/2), sec)
			menu['bg'] = MENU_FULL_COLOR
			var.set(str(int(sec))+' Sec.')
			self.iniClass.changeOptValue(selction,option, str(sec/2))
		return

	### Add Menu for times of thermal cycle from configure file 
	def addnCycleMenu(self, frame, label="", name0="", name1="", row=0, column=0, value='', nmax=CYCLE_MAX, sticky='wn', width=10):
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
		newMenu['fg']=TITLE4_COLOR
		newMenu['font']=BUTTON_FONT
		if not value.isdigit():
			print ">> [ERROR] "+label+" '"+name+"' has wrong value '"+value+"'"
			print ">>         Please select the number to fix it" 
			var.set("ERROR")
		else:
			newMenu['bg'] = MENU_FULL_COLOR
			var.set(str(int(value)))
		newMenu.grid( row=row, column=column, sticky=sticky)
		newMenu['menu'].delete(0)
		ilabel=1
		while ( ilabel <= nmax ):
			newMenu['menu'].add_command(label=str(ilabel),command=lambda ilabel=ilabel:self.chooseCycle(newMenu,str(ilabel),name0,name1,var))
			ilabel+=1
		self.Menu[name]=newMenu

	def chooseCycle(self, menu, label, selction, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return
		value = self.iniClass.Sections[selction][option]
		if value != label:
			print ">> [INFO] Change %s : %s : %s -> %s "%(selction, option, value, label)
			menu['bg'] = MENU_FULL_COLOR
			var.set(label)
			self.iniClass.changeOptValue(selction,option,label)
		return

	### Add Menu for muduel tyes from configure file 
	def addMuduelTypeMenu(self, frame, label="", name0="", name1="", row=0, column=0, columnspan=1, value='', sticky='wn', width=10):
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
		newMenu['fg']=TITLE4_COLOR
		newMenu['font']=BUTTON_FONT
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
		newMenu.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		newMenu['menu'].delete(0)
		newMenu['menu'].add_command( label="Full", command=lambda:self.chooseType( newMenu, 'Full', name0, name1, var))
		newMenu['menu'].add_command( label="Roc",  command=lambda:self.chooseType( newMenu, 'Roc', name0, name1, var,))
		self.Menu[name]=newMenu

	def chooseType(self, menu, label, selction, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return
		value = self.iniClass.Sections[selction][option]
		if value != label:
			print ">> [INFO] Change %s : %s : %s -> %s "%(selction, option, value, label)
			if label == 'Full':
				menu['bg'] = MENU_FULL_COLOR
			if label == 'Roc':
				menu['bg'] = MENU_ROC_COLOR
			var.set(label)
			self.iniClass.changeOptValue(selction,option,label)
		return
	
	def expendWindow(self, frame, maxRow, maxCol):
		for x in range(maxCol):
		  Grid.columnconfigure(frame, x, weight=1)

		for y in range(maxRow):
		  Grid.rowconfigure(frame, y, weight=1)
		return
		

	######## * Main function and platform ####### ======================================================================================
	def createWidgets(self):
		# Title
		mainRow=0
		self.title = Label(self.master, bg=BG_framMain, font=('helvetica', 15, 'bold'), fg=TITLE_COLOR )
		self.title["text"]="elComandante.ini"
		self.title.grid(row=mainRow, column=0, columnspan=COLUMNMAX, sticky=NSEW )

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		### * Configuration * -------------------------------------------------------------------------------------------------------
		mainRow+=1
		self.addLabel(label='Main', name1='Input Configure', frame=self.master, row=mainRow, column=1, font=SECTION_FONT, sticky='ew')

		self.entryConfig = Entry(self.master, bg=ENTRY_COLOR)
		self.entryConfig["width"]=15
		self.entryConfig.insert(0, self.loadConfig)
		self.entryConfig.grid(row=mainRow, column=2, columnspan=2, sticky='ew' )
		self.entryConfig.bind('<Key>', lambda event:self.chEntryBG(self.entryConfig))
		self.entryConfig.bind('<Leave>', lambda event:self.checkChanging(self.entryConfig,self.loadConfig ))

		self.buttonReload = Button(self.master, bg=RELOAD_COLOR, font=BUTTON2_FONT, fg=TITLE4_COLOR)
		self.buttonReload["text"]="ReLoad"
		self.buttonReload.grid(row=mainRow, column=4, sticky=EW)
	
		self.buttonLock = Button(self.master, font=BUTTON2_FONT, fg=TITLE4_COLOR, command=self.lock)
		if self.isfixed == True:
			self.buttonLock["text"]="Unlock"
			self.buttonLock["bg"]=UNLOCK_COLOR
		else:
			self.buttonLock["text"]="Lock"
			self.buttonLock["bg"]=LOCK_COLOR
		self.buttonLock.grid(row=mainRow, column=5, sticky=EW)

		self.buttonNext = Button(self.master, bg=PREVIEW_COLOR, fg=TITLE4_COLOR, font=BUTTON2_FONT)
		self.buttonNext["text"]="Next"
		self.buttonNext.grid(row=mainRow, column=6, sticky=EW)

		self.locklabel = Label(self.master, bg=BG_framMain, font=('helvetica', 15, 'bold'), fg='red' )
		self.locklabel["text"]="Locked!"
		self.locklabel.grid(row=mainRow, column=7, sticky=EW )

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		### * elComandante_ini * -------------------------------------------------------------------------------------------------------

		### DTB = ['Modules', 'ModuleType', 'TestboardUse']
		mainRow+=1
		self.DTB = Frame( self.master, bg=BG_framMain)
		self.DTB.grid( row=mainRow, column=1, sticky=N+S+E+W, columnspan=6 )

		startCol=0
		mainRow+=1
		irow=1
		icol=startCol+1
		self.addLabel( label='Main_DTB', name1='Modules', frame=self.DTB, font=SECTION_FONT, column=startCol, row=irow, sticky='ew' )
		for opt in self.iniClass.list_Default['Modules']:
			value=self.iniClass.Sections['Modules'][opt]
			self.addLabel(label='Main_DTB', name0='Modules', name1=opt, frame=self.DTB, row=irow-1, column=icol, sticky='ew')
			self.addOptEntry(label='Main_DTB', name0='Modules', name1=opt, frame=self.DTB, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1

		icol=startCol+1
		self.addLabel( label='Main_DTB', name1='ModuleType', frame=self.DTB, font=SECTION_FONT, column=startCol, row=irow, sticky='ew' )
		for opt in self.iniClass.list_Default['ModuleType']:
			value=self.iniClass.Sections['ModuleType'][opt]
			self.addMuduelTypeMenu( label='Main_DTB', name0='ModuleType', name1=opt, frame=self.DTB, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1

		icol=startCol+1
		self.addLabel( label='Main_DTB', name1='TestboardUse', frame=self.DTB, font=SECTION_FONT, column=startCol, row=irow,sticky='ew' )
		for opt in self.iniClass.list_Default['TestboardUse']:
			value=self.iniClass.Sections['TestboardUse'][opt]
			self.addBoolButton( label='Main_DTB', name0='TestboardUse', name1=opt, frame=self.DTB, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1
		self.expendWindow(self.DTB, irow, icol)

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		### Device = ['CoolingBox', 'Keithley', 'LowVoltage', 'Xray']
		mainRow+=1
		self.Device = Frame( self.master, bg=BG_framMain)
		self.Device.grid( row=mainRow, column=1, sticky=N+S+E+W, columnspan=6 )

		startCol=0
		self.addLabel( label='Main_Device', name1='CoolingBox', frame=self.Device, font=SECTION_FONT, column=startCol, row=0, sticky='ew' )
		self.addLabel( label='Main_Device', name1='Keithley',   frame=self.Device, font=SECTION_FONT, column=startCol+1, row=0, sticky='ew', columnspan=1 )
		self.addLabel( label='Main_Device', name1='LowVoltage', frame=self.Device, font=SECTION_FONT, column=startCol+2, row=0, sticky='ew' )
		self.addLabel( label='Main_Device', name1='Xray',       frame=self.Device, font=SECTION_FONT, column=startCol+3, row=0, sticky='ew' )
		irow=1
		icol=startCol
		for opt in self.iniClass.list_Default['CoolingBox']:
			value=self.iniClass.Sections['CoolingBox'][opt]
			self.addLabel(label='Main_Device', name0='CoolingBox', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			self.addBoolButton( label='Main_Device', name0='CoolingBox', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1

		irow=1
		for opt in self.iniClass.list_Default['Keithley']:
			value=self.iniClass.Sections['Keithley'][opt]
			self.addLabel(label='Main_Device', name0='Keithley', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			if opt == 'KeithleyUse':
				self.addLabel(label='Main_Device', name0='Keithley', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
				self.addBoolButton( label='Main_Device', name0='Keithley', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			else:
				self.addLabel(label='Main_Device', name0='Keithley', name1=opt+'(Volt)', frame=self.Device, row=irow, column=icol, sticky='ew')
				self.addOptEntry(label='Main_Device', name0='Keithley', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1

		irow=1
		for opt in self.iniClass.list_Default['LowVoltage']:
			value=self.iniClass.Sections['LowVoltage'][opt]
			self.addLabel(label='Main_Device', name0='LowVoltage', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			self.addBoolButton( label='Main_Device', name0='LowVoltage', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1
	
		irow=1
		for opt in self.iniClass.list_Default['Xray']:
			value=self.iniClass.Sections['Xray'][opt]
			self.addLabel(label='Main_Device', name0='Xray', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			self.addBoolButton( label='Main_Device', name0='Xray', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1
		self.expendWindow(self.Device, 5, icol)

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		### Process = ['Cycle', 'IV', 'Tests', 'OperationDetails']
		mainRow+=1
		self.Process = Frame( self.master, bg=BG_framMain, relief=SUNKEN, borderwidth=2)
		self.Process.grid( row=mainRow, column=1, sticky=N+S+E+W, columnspan=6 )

		mainRow+=1
		irow=1
		self.addLabel( label='Main_Process', name1='Cycle', frame=self.Process, font=SECTION_FONT, column=0, row=irow )
		icol=1
		for opt in self.iniClass.list_Default['Cycle']:
			value=self.iniClass.Sections['Cycle'][opt]
			if opt == 'nCycles':
				self.addLabel(label='Main_Process', name0='Cycle', name1=opt, frame=self.Process, row=0, column=icol)
				self.addnCycleMenu( label='Main_Process', name0='Cycle', name1=opt, frame=self.Process, value=value, row=irow, column=icol)
			else:
				self.addLabel(label='Main_Process', name0='Cycle', name1=opt+u" (\N{DEGREE SIGN}C)", frame=self.Process,row=0,column=icol)
				self.addOptEntry(label='Main_Process', name0='Cycle', name1=opt, frame=self.Process, value=value, row=irow, column=icol )
			icol+=1
		irow+=2

		self.addLabel( label='Main_Process', name1='IV', frame=self.Process, font=SECTION_FONT, column=0, row=irow )
		icol=1
		for opt in self.iniClass.list_Default['IV']:
			value=self.iniClass.Sections['IV'][opt]
			if opt == 'Delay':
				self.addLabel(label='Main_Process', name0='IV', name1=opt, frame=self.Process, row=irow-1, column=icol)
				self.addDelayMenu( label='Main_Process', name0='IV', name1=opt, frame=self.Process, value=value, row=irow, column=icol)
			else:
				self.addLabel(label='Main_Process', name0='IV', name1=opt+' (Volt)', frame=self.Process, row=irow-1, column=icol)
				self.addOptEntry(label='Main_Process', name0='IV', name1=opt, frame=self.Process, value=value, row=irow, column=icol)
			icol+=1
		irow+=1

		for opt in self.iniClass.list_Default['Tests']:
			self.addLabel(label='Main_Process', name0='Tests', name1=opt, frame=self.Process, row=irow, font=SECTION_FONT)
			value=self.iniClass.Sections['Tests'][opt]
			if opt == 'Test':
				self.addOptEntry(label='Main_Process', name0='Tests', name1=opt, frame=self.Process, value=value, row=irow, column=1, width=20, columnspan=6, isFixed=True)
				irow+=1
				self.addLabel(label='Main_Process', name0='Tests', name1='Options', frame=self.Process, row=irow, rowspan=2, sticky='ns', font=SECTION_FONT)
				self.addTestButton(label='Main_Process', name0='Tests', name1='IV@17', frame=self.Process, row=irow, column=1, sticky='ew')
				self.addTestButton(label='Main_Process', name0='Tests', name1='Pretest@17', frame=self.Process, row=irow, sticky='ew', column=2 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Fulltest@17', frame=self.Process, row=irow, sticky='ew', column=3 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Cycle', frame=self.Process,row=irow,column=4,sticky='nsew', rowspan=2 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Add new test', frame=self.Process,row=irow,column=5, columnspan=2, sticky='we')
				irow+=1
				self.addTestButton(label='Main_Process', name0='Tests', name1='IV@-20', frame=self.Process, row=irow, sticky='ew', column=1 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Pretest@-20', frame=self.Process, row=irow, sticky='ew', column=2 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Fulltest@-20', frame=self.Process, row=irow, sticky='ew', column=3 )
				self.addEntry(label='Main_Process', name0='Tests', name1='New Test', frame=self.Process, value='Ex: IV@10', row=irow, column=5, sticky='ew', columnspan=2 )
			elif opt == 'TestDescription':
				self.addOptEntry(label='Main_Process', name0='Tests', name1=opt, frame=self.Process, value=value, row=irow, column=1, columnspan=4)
				self.addTestButton(label='Main_Process', name0='Tests', name1='Delete', frame=self.Process, row=irow, column=5 )
				self.addTestButton(label='Main_Process', name0='Tests', name1='Clear', frame=self.Process, row=irow, column=6 )
			else:
				self.addOptEntry(label='Main_Process', name0='Tests', name1=opt, frame=self.Process, value=value, row=irow, column=1)
			irow+=1
	
		self.expendWindow(self.Process, irow, 7)

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		### Operation = ['Hostname', 'TestCenter', 'Jui-Fa Tsai']
		mainRow+=1
		self.Operation = Frame( self.master, bg=BG_framMain)
		self.Operation.grid( row=mainRow, column=1, sticky=N+S+E+W, columnspan=6 )

		mainRow+=1
		irow=1
		icol=1
		self.addLabel( label='Main_Operation', name1='OperationDetails', frame=self.Operation, font=SECTION_FONT, column=0, row=irow, sticky='ew' )
		for opt in self.iniClass.list_Default['OperationDetails']:
			value=self.iniClass.Sections['OperationDetails'][opt]
			self.addLabel(label='Main_Operation', name0='OperationDetails', name1=opt, frame=self.Operation, row=irow-1, column=icol, sticky='ew')
			self.addOptEntry(label='Main_Operation', name0='OperationDetails', name1=opt, frame=self.Operation, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1
		self.expendWindow(self.Operation, irow, icol)

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		# Options 
		mainRow+=1
		self.addSave( self.master, row=mainRow, column=COLUMNMAX-4,sticky='e')
		self.addPreview( self.master, row=mainRow, column=COLUMNMAX-3, sticky='ew')
		self.addQUIT( self.master, row=mainRow, column=COLUMNMAX-2, sticky='w' )

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		# For objects can expend with window
		mainRow+=1
		self.expendWindow(self.master, mainRow, COLUMNMAX)

		return
####### example ########
if __name__ == '__main__':
	root = Tk()
	app = interface(master=root)
	app.loadConfig("./elComandante.ini.default")
	app.createWidgets()
	root.mainloop()
