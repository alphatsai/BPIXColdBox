#!/usr/bin/env python
import os, re, sys, shutil, commands
import math, ROOT

from Tkinter import *
import tkFont

sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from readConfg import elComandante_ini
from readConfg import elComandante_conf

Delay_MAX=8 #sec
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
BG_MASTER='gray93'
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
		self.master["bg"]=BG_MASTER
		self.master.grid()
		self.isfixed=True
		self.isfixed=True
		self.iniClass = None
		self.confClass = None
		self.output=None
		self.frames={}
		self.framesButton={}
		self.Labels={}
		self.Entries={}
		self.OptEntries={}
		self.BoolButtons={}
		self.testButtons={}
		self.Menu={}
		self.Var={}
		self.testPath='./example/tests'
		self.confingurePath = { 'elComandante.ini' :'./elComandante.ini.default',
					'elComandante.conf':'./elComandante.conf.default'
					}
		self.whichConfig = { 'elComandante.ini':True,
				     'elComandante.conf':False
				   }
		self.loadElcommandateIni();
		self.loadElcommandateConf();
	
	#### Load configure file
	def loadElcommandateIni(self):
		self.iniClass = elComandante_ini()
		self.iniClass.getDefault(self.confingurePath['elComandante.ini'])
		self.loadTestsOptions()
		return

	def loadElcommandateConf(self):
		self.confClass = elComandante_conf()
		self.confClass.getDefault(self.confingurePath['elComandante.conf'])
		self.loadTestsOptions()
		return

	def loadTestsOptions(self):
		listDir = commands.getoutput('ls '+self.testPath)
		self.tests = listDir.split('\n')
		return

	### Add empty pad for designing 
	def addXpad(self, frame, colmax=8, bg=BG_MASTER, width=10, height=1, row=0):
		col=0
		while ( col < colmax ):
			pad = Label(frame, bg=bg, width=width, height=height)
			pad.grid(row=row, column=col)
			col+=1
		return
	
	### Make all frame and tk can be expended with window
	def expendWindow(self, frame, maxRow, maxCol):
		for x in range(maxCol):
			Grid.columnconfigure(frame, x, weight=1)

		for y in range(maxRow):
			Grid.rowconfigure(frame, y, weight=1)
		return
		
	### Change elcommandate.ini and elcommandate.conf
	def changeFrame(self, name):
		frame = self.frames[name]
		frame.tkraise()
		for button in self.framesButton:
			if button == name:
				self.framesButton[button]['bg']=BG_MASTER
				self.framesButton[button]['fg']=TITLE4_COLOR
				self.whichConfig[button]=True
				self.Labels[button].tkraise()
				self.entryConfig.delete(0, END)
				self.entryConfig.insert(0, self.confingurePath[button])
			else:
				self.framesButton[button]['bg']=ENTRY_LOCKED_COLOR
				self.framesButton[button]['fg']=TITLE_COLOR
				self.whichConfig[button]=False
		#if not self.isfixed:
		#	self.lock()
		return

	### ReLoad button
	def reLoadConfig(self):
		if self.isfixed:
			print '>> [INFO] The button is locked!'
			return
		if self.whichConfig['elComandante.ini']:
			if os.path.isfile( self.entryConfig.get() ):
				self.confingurePath['elComandante.ini'] = self.entryConfig.get()
				self.loadElcommandateIni()
				# refresh option entries
				for name in self.OptEntries:
					entry = self.OptEntries[name]
					section = name.split('_')[2]
					option = name.split('_')[3]
					entry.delete(0, END)
					entry.insert(0, self.iniClass.Sections[section][option])
				# refresh add new test entry
				self.lastClickNewTest='Ex: IV@10'
				self.Entries['ini_Process_Tests_NewTest'].delete(0,END)
				self.Entries['ini_Process_Tests_NewTest'].insert(0, 'Ex: IV@10')
				# refresh BoolButtons 
				for name in self.BoolButtons:
					button = self.BoolButtons[name]
					section = name.split('_')[2]
					option = name.split('_')[3]
					self.fillBoolName(button, section, option, self.iniClass.Sections[section][option])
				# refresh menu 
				for name in self.Menu:
					menu = self.Menu[name]
					var = self.Var[name]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if section == 'IV':
						self.setDelayVar( menu, var, section, option, self.iniClass.Sections[section][option])
					elif section == 'Cycle':
						self.setCycleVar( menu, var, section, option, self.iniClass.Sections[section][option])
					elif section == 'ModuleType':
						self.setTypeVar( menu, var, section, option, self.iniClass.Sections[section][option])
			else:
				print ">> [ERROR] Can't find '%s'"% self.entryConfig.get()
				return
		elif self.whichConfig['elComandante.conf']:
			print '>> [INFO] Comming soon!'
		self.lock()
		self.isfixed=True

	### Lock button
	def lock(self):
		# UnLocked
		if self.buttonLock['text'] == 'Unlock': 
			self.isfixed=False
			self.buttonLock['text']='Lock'
			self.buttonLock['bg']=LOCK_COLOR
			self.locklabel['fg']=BG_MASTER
			self.entryConfig['bg']=ENTRY_COLOR
			for entry in self.Entries:
				self.Entries[entry]['bg']=ENTRY_COLOR
		# Locked
		else:
			self.isfixed=True
			self.buttonLock['text']='Unlock'
			self.buttonLock['bg']=UNLOCK_COLOR
			self.locklabel['fg']='red'
			self.entryConfig['bg']=ENTRY_LOCKED_COLOR
			for entry in self.Entries:
				self.Entries[entry]['bg']=ENTRY_LOCKED_COLOR
			if int(self.lastClickNewCycle) <= 10:
				self.Labels['ini_Process_Cycle_HideOther'].tkraise()
				self.Var['ini_Process_Cycle_nCycles'].set(self.lastClickNewCycle)
				self.Menu['ini_Process_Cycle_nCycles']['bg']=MENU_FULL_COLOR
	
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
		if self.whichConfig['elComandante.ini']:
			self.iniClass.callConfig()
		if self.whichConfig['elComandante.conf']:
			self.confClass.callConfig()
		return

	### Save button
	def addSave(self, frame, row=0, column=0, text="Save", bg=SAVE_COLOR, font=BUTTON2_FONT, columnspan=1, sticky='se', width=5):
		self.SAVE = Button(frame, font=font, bg=bg, text=text, width=width, fg=TITLE4_COLOR, command= lambda:self.saveConfig(self.output) )
		self.SAVE.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

	def saveConfig(self, output=None):
		if self.whichConfig['elComandante.ini']:
			self.iniClass.makeConfig(output)
		if self.whichConfig['elComandante.conf']:
			self.confClass.makeConfig(output)
		return

	### Add commend label 
	def addLabel(self, frame, label="", name0="", name1="", row=0, column=0, sticky='nsew', columnspan=1, rowspan=1, bg=BG_MASTER, font=OPTION_FONT, fg=TITLE3_COLOR):
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
		self.OptEntries[name]=newEntry
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
		newvalue = entry.get().strip()
		if value != newvalue and newvalue !='':
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
		newButton['fg']=TITLE4_COLOR
		newButton['font']=BUTTON_FONT
		newButton['command']=lambda:self.changeBool( name, name0, name1 )
		self.fillBoolName(newButton, name0, name1, value)
		newButton.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		self.BoolButtons[name]=newButton

	def fillBoolName(self, button, section, option, value):
		button['text']="OFF"
		button['bg']=FALSE_COLOR
		if value.lower() !=  "true" and value.lower() != "false":
			print ">> [ERROR] "+section+" '"+option+"' has wrong value '"+value+"'"
			print ">>         Please click the button to fix it" 
			button['text']='ERROR'
			button['bg']=ERROR_COLOR
		elif value == "True":
			button['text']="ON"
			button['bg']=TRUE_COLOR
		return

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

		newButton = Button(frame)
		newButton['width'] =width
		newButton['text']=name1
		newButton['bg']=FALSE_COLOR
		newButton['fg']=TITLE4_COLOR
		newButton['font']=BUTTON_FONT
		newButton.grid( row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan)
		if self.checkTests(newButton, name1):
			newButton['command']=lambda:self.activeTestButton(newButton)
			newButton.bind('<Button-1>', lambda event:self.changeColorTestEntry(0))
			newButton.bind('<Leave>', lambda event:self.changeColorTestEntry(1))
		self.testButtons[name]=newButton
		return

	def checkTests(self, button, tests):
		test = tests.split('@')[0]
		testfile =  self.testPath+'/'+test
		if test=='IV' or test== 'Cycle' or test=='Add new test' or test=='Delete' or test=='Clear':
			return True
		elif not os.path.isfile(testfile):
			print ">> [ERROR] Can't find '"+test+"' in '"+self.testPath+"', or it's not a file..."
			button['text']=test+'??'
			button['bg']=ERROR_COLOR
			return False
		else:
			return True

	def activeTestButton(self, button):
		if self.isfixed:
			print '>> [INFO] The button is locked!'
			return

		if button['text'] == 'Clear':
			self.Entries['ini_Process_Tests_Test'].delete(0,END)
			self.iniClass.changeOptValue('Tests','Test', '')
			print ">> [INFO] Clear Tests! "
			print ">>        Changed Tests : "
			return

		tests = self.Entries['ini_Process_Tests_Test'].get()
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
			self.Entries['ini_Process_Tests_Test'].delete(0,END)
			self.Entries['ini_Process_Tests_Test'].insert(0, restTests)
			self.iniClass.changeOptValue('Tests','Test', restTests)
			print ">> [INFO] Delete a test '%s'"%(delTest)
			print ">>        Changed Tests %s: "%(restTests)
			return

		newprocess=''
		if button['text'] == 'Add new test':
			self.lastClickNewTest = self.Entries['ini_Process_Tests_NewTest'].get()
			if self.lastClickNewTest == '':
				return
			i=1
			newalltests = self.lastClickNewTest.split(',')
			for newTests in newalltests:
				newtests = newTests.strip().split('@') #remove backspace in front/end first
				newtest  = newtests[0]
				if len(newtests) > 2:
					self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
					print '>> [ERROR] Too many arguments'
					print '>>         E.x: Fulltest@17,IV@10'
					self.lastClickNewTest=''
					return
				elif len(newtests) == 2:
					temperature = newtests[1]
					if not temperature.isdigit():
						self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
						print '>> [ERROR] After @ shall be digit, i.e temperature'
						print '>>         E.x: Fulltest@17'
						self.lastClickNewTest=''
						return

				if newtest in self.tests or newtest == 'IV' or newtest == 'Cycle':
					if newtest == 'Cycle' and len(newtests)!=1:
						self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
						print ">> [ERROR] Cycle shall not add @ and temperature"
						self.lastClickNewTest=''
						return
					
					if len(newalltests) > 1 and i<len(newalltests):
						newprocess += newTests.strip()+','
					else:
						newprocess += newTests.strip()
					i+=1
					self.Entries['ini_Process_Tests_NewTest']['bg']=ENTRY_COLOR
				else:
					self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
					print ">> [ERROR] Not found '"+newtest+"' in "+self.testPath
					print ">>         Please add it in '"+self.testPath+"' and reload"
					self.lastClickNewTest=''
					return
		else: 
			newprocess = button['text']

		if tests ==  '':
			tests=newprocess
		else:
			tests+=','+newprocess

		self.Entries['ini_Process_Tests_Test'].delete(0,END)
		self.Entries['ini_Process_Tests_Test'].insert(0, tests)
		self.iniClass.changeOptValue('Tests','Test', tests)
		print ">> [INFO] Add new process %s "%(newprocess)
		print ">>        Changed Tests : %s "%(tests)
		return
	
	def changeColorTestEntry(self, action):
		if self.isfixed:
			return

		if action == 0: #<Button-1>
			self.Entries['ini_Process_Tests_Test']['bg']=BYTYPING_COLOR
		elif action == 1: #<Leave>
			self.Entries['ini_Process_Tests_Test']['bg']=ENTRY_COLOR
		
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
		newMenu['menu'].delete(0)
		sec=1.
		while ( sec <= nmax ):
			newMenu['menu'].add_command(label=str(int(sec))+' Sec.',command=lambda sec=sec:self.chooseDelay( newMenu, sec, name0, name1, var))
			sec+=1
		newMenu.grid( row=row, column=column, sticky=sticky)
		self.setDelayVar(newMenu, var, name0, name1, value)
		self.Menu[name]=newMenu
		self.Var[name]=var
	
	def setDelayVar(self, menu, var, section, option, value):
		menu['bg'] = ERROR_COLOR
		menu['fg']=TITLE4_COLOR
		menu['font']=BUTTON_FONT
		if not value.isdigit():
			print ">> [ERROR] "+section+" '"+option+"' has wrong value '"+value+"'"
			print ">>         Please select the number to fix it" 
			var.set("ERROR")
		else:
			menu['bg'] = MENU_FULL_COLOR
			var.set(str(int(float(value)*2))+' Sec.')

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
	def addnCycleMenu(self, frame, label="", name0="", name1="", row=0, column=0, value='', nmax=10, sticky='wn', width=10):
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
		newMenu['menu'].delete(0)
		ilabel=1
		while ( ilabel <= nmax ):
			newMenu['menu'].add_command(label=str(ilabel),command=lambda ilabel=ilabel:self.chooseCycle(newMenu,str(ilabel),name0,name1,var))
			ilabel+=1
		newMenu['menu'].add_command(label='Other', command=lambda ilabel=ilabel:self.chooseCycle(newMenu,'Other',name0,name1,var))
		newMenu.grid( row=row, column=column, sticky=sticky)
		self.setCycleVar(newMenu, var, name0, name1, value)
		self.Menu[name]=newMenu
		self.Var[name]=var

	def setCycleVar(self, menu, var, section, option, value):
		menu['bg'] = ERROR_COLOR
		menu['fg']=TITLE4_COLOR
		menu['font']=BUTTON_FONT
		if not value.isdigit():
			print ">> [ERROR] "+section+" '"+option+"' has wrong value '"+value+"'"
			print ">>         Please select the number to fix it" 
			self.lastClickNewCycle=''
			var.set("ERROR")
		elif int(value)>10:
			menu['bg'] = FALSE_COLOR
			self.Entries['ini_Process_Cycle_Other'].delete(0, END)
			self.Entries['ini_Process_Cycle_Other'].insert(0, str(int(value)))
			self.Entries['ini_Process_Cycle_Other'].tkraise()
			self.lastClickNewCycle=str(int(value))
			var.set('Other')
		else:
			self.Labels['ini_Process_Cycle_HideOther'].tkraise()
			self.Entries['ini_Process_Cycle_Other'].delete(0, END)
			self.lastClickNewCycle=str(int(value))
			menu['bg'] = MENU_FULL_COLOR
			var.set(str(int(value)))
		return

	def chooseCycle(self, menu, label, selction, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return
		value = self.iniClass.Sections[selction][option]
		if value != label:
			var.set(label)
			if label == 'Other':
				menu['bg'] = FALSE_COLOR
				self.Entries['ini_Process_Cycle_Other'].tkraise()
			else:
				print ">> [INFO] Change %s : %s : %s -> %s "%(selction, option, value, label)
				menu['bg'] = MENU_FULL_COLOR
				self.iniClass.changeOptValue(selction,option,label)
				self.Entries['ini_Process_Cycle_Other'].delete(0, END)
				self.Entries['ini_Process_Cycle_Other'].insert(0, '')
				self.Labels['ini_Process_Cycle_HideOther'].tkraise()
				self.lastClickNewCycle=label
		return

	def chooseOtherCycle(self, entry):
		newvalue = entry.get().strip()
		value = self.iniClass.Sections['Cycle']['nCycles']
		if  value != newvalue and newvalue != '':
			if not newvalue.isdigit(): 
				print '>> [ERROR] Shall be a digit number, i.e times'
				return
			print ">> [INFO] Change Cycle : nCycles : %s -> %s "%( value, newvalue)
			self.iniClass.changeOptValue('Cycle', 'nCycles', newvalue)
			self.lastClickNewCycle=newvalue
			entry['bg']=ENTRY_COLOR
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
		newMenu['menu'].delete(0)
		newMenu['menu'].add_command( label="Full", command=lambda:self.chooseType( newMenu, 'Full', name0, name1, var))
		newMenu['menu'].add_command( label="Roc",  command=lambda:self.chooseType( newMenu, 'Roc', name0, name1, var,))
		newMenu.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		self.setTypeVar( newMenu, var, name0, name1, value)
		self.Menu[name]=newMenu
		self.Var[name]=var
	
	def setTypeVar(self, menu, var, section, option, value):
		menu['bg'] = ERROR_COLOR
		menu['fg']=TITLE4_COLOR
		menu['font']=BUTTON_FONT
		if value.lower() !=  "full" and value.lower() != "roc":
			print ">> [ERROR] "+section+" '"+option+"' has wrong value '"+value+"'"
			print ">>         Please select the type to fix it"
			var.set("ERROR")
		elif value=="Full":
			menu['bg'] = MENU_FULL_COLOR
			var.set(value)
		elif value=="Roc":
			menu['bg'] = MENU_ROC_COLOR
			var.set(value)
		return

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

	######## * ini function and platform ####### ======================================================================================
	def createWidgets(self):
		# Pad 
		#mainRow+=1
		mainRow=0
		self.addXpad( self.master, row=mainRow)

		### * Configuration * -------------------------------------------------------------------------------------------------------
		mainRow+=1
		self.addLabel(label='', name1='elComandante.conf', frame=self.master, row=mainRow, column=1, font=SECTION_FONT, sticky='ew')
		self.addLabel(label='', name1='elComandante.ini', frame=self.master, row=mainRow, column=1, font=SECTION_FONT, sticky='ew')

		self.entryConfig = Entry(self.master)
		if self.isfixed:
			self.entryConfig["bg"]=ENTRY_LOCKED_COLOR
		else:
			self.entryConfig["bg"]=ENTRY_COLOR
		self.entryConfig["width"]=15
		self.entryConfig.insert(0, self.confingurePath['elComandante.ini'])
		self.entryConfig.grid(row=mainRow, column=2, columnspan=3, sticky='ew' )
		self.entryConfig.bind('<Key>', lambda event:self.chEntryBG(self.entryConfig, self.confingurePath['elComandante.ini']))
		self.entryConfig.bind('<Leave>', lambda event:self.checkChanging(self.entryConfig, self.confingurePath['elComandante.ini'] ))

		self.buttonReload = Button(self.master, bg=RELOAD_COLOR, font=BUTTON2_FONT, fg=TITLE4_COLOR, command=self.reLoadConfig)
		self.buttonReload["text"]="Load"
		self.buttonReload.grid(row=mainRow, column=5, sticky=EW)
	
		self.buttonLock = Button(self.master, font=BUTTON2_FONT, fg=TITLE4_COLOR, command=self.lock)
		if self.isfixed == True:
			self.buttonLock["text"]="Unlock"
			self.buttonLock["bg"]=UNLOCK_COLOR
		else:
			self.buttonLock["text"]="Lock"
			self.buttonLock["bg"]=LOCK_COLOR
		self.buttonLock.grid(row=mainRow, column=6, sticky=EW)

		self.locklabel = Label(self.master, bg=BG_MASTER, font=('helvetica', 15, 'bold'), fg='red' )
		self.locklabel["text"]="Locked!"
		self.locklabel.grid(row=mainRow, column=7, sticky=EW )

		# Pad 
		mainRow+=1
		self.addXpad( self.master, row=mainRow)

		# Button for changing elComandante_ini or elComandante_config 
		mainRow+=1
		self.buttonIni = Button(self.master, bg=BG_MASTER, fg=TITLE4_COLOR, font=BUTTON2_FONT, command=lambda: self.changeFrame('elComandante.ini'))
		self.buttonIni["text"]="elComandante.ini"
		self.buttonIni.grid(row=mainRow, column=0, sticky=EW, columnspan=4)
		self.framesButton['elComandante.ini']=self.buttonIni
		self.buttonConf = Button(self.master, bg=ENTRY_LOCKED_COLOR, fg=TITLE_COLOR, font=BUTTON2_FONT, command=lambda: self.changeFrame('elComandante.conf'))
		self.buttonConf["text"]="elComandante.conf"
		self.buttonConf.grid(row=mainRow, column=4, sticky=EW, columnspan=5)
		self.framesButton['elComandante.conf']=self.buttonConf

		# * Set frame for elComandante.ini and elComandante.conf
		mainRow+=1
		self.ElIni = Frame( self.master, bg=BG_MASTER, relief=RAISED, borderwidth=2 )
		self.ElIni.grid( row=mainRow, column=0, sticky=N+S+E+W, columnspan=COLUMNMAX )
		self.ElConf = Frame( self.master, bg=BG_MASTER, relief=RAISED, borderwidth=2 )
		self.ElConf.grid( row=mainRow, column=0, sticky=N+S+E+W, columnspan=COLUMNMAX )
		self.frames["elComandante.ini"]=self.ElIni
		self.frames["elComandante.conf"]=self.ElConf

		### * elComandante_ini * -------------------------------------------------------------------------------------------------------

		self.buttonIni.tkraise()
		self.ElIni.tkraise()  # Show elComandante.ini first

		### DTB = ['Modules', 'ModuleType', 'TestboardUse']
		# Pad 
		eliniRow=0
		self.addXpad( self.ElIni, row=eliniRow)

		eliniRow+=1
		self.DTB = Frame( self.ElIni, bg=BG_MASTER)
		self.DTB.grid( row=eliniRow, column=1, sticky=N+S+E+W, columnspan=6 )

		startCol=0
		irow=1
		icol=startCol+1
		self.addLabel( label='ini_DTB', name1='Modules', frame=self.DTB, font=SECTION_FONT, column=startCol, row=irow, sticky='ew' )
		for opt in self.iniClass.list_Default['Modules']:
			value=self.iniClass.Sections['Modules'][opt]
			self.addLabel(label='ini_DTB', name0='Modules', name1=opt, frame=self.DTB, row=irow-1, column=icol, sticky='ew')
			self.addOptEntry(label='ini_DTB', name0='Modules', name1=opt, frame=self.DTB, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1

		icol=startCol+1
		self.addLabel( label='ini_DTB', name1='ModuleType', frame=self.DTB, font=SECTION_FONT, column=startCol, row=irow, sticky='ew' )
		for opt in self.iniClass.list_Default['ModuleType']:
			value=self.iniClass.Sections['ModuleType'][opt]
			self.addMuduelTypeMenu( label='ini_DTB', name0='ModuleType', name1=opt, frame=self.DTB, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1

		icol=startCol+1
		self.addLabel( label='ini_DTB', name1='TestboardUse', frame=self.DTB, font=SECTION_FONT, column=startCol, row=irow,sticky='ew' )
		for opt in self.iniClass.list_Default['TestboardUse']:
			value=self.iniClass.Sections['TestboardUse'][opt]
			self.addBoolButton( label='ini_DTB', name0='TestboardUse', name1=opt, frame=self.DTB, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1
		self.expendWindow(self.DTB, irow, icol)

		# Pad 
		eliniRow+=1
		self.addXpad( self.ElIni, row=eliniRow)

		### Device = ['CoolingBox', 'Keithley', 'LowVoltage', 'Xray']
		eliniRow+=1
		self.Device = Frame( self.ElIni, bg=BG_MASTER)
		self.Device.grid( row=eliniRow, column=1, sticky=N+S+E+W, columnspan=6 )

		startCol=0
		self.addLabel( label='ini_Device', name1='CoolingBox', frame=self.Device, font=SECTION_FONT, column=startCol, row=0, sticky='ew' )
		self.addLabel( label='ini_Device', name1='Keithley',   frame=self.Device, font=SECTION_FONT, column=startCol+1, row=0, sticky='ew', columnspan=1 )
		self.addLabel( label='ini_Device', name1='LowVoltage', frame=self.Device, font=SECTION_FONT, column=startCol+2, row=0, sticky='ew' )
		self.addLabel( label='ini_Device', name1='Xray',       frame=self.Device, font=SECTION_FONT, column=startCol+3, row=0, sticky='ew' )
		irow=1
		icol=startCol
		for opt in self.iniClass.list_Default['CoolingBox']:
			value=self.iniClass.Sections['CoolingBox'][opt]
			self.addLabel(label='ini_Device', name0='CoolingBox', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			self.addBoolButton( label='ini_Device', name0='CoolingBox', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1

		irow=1
		for opt in self.iniClass.list_Default['Keithley']:
			value=self.iniClass.Sections['Keithley'][opt]
			self.addLabel(label='ini_Device', name0='Keithley', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			if opt == 'KeithleyUse':
				self.addLabel(label='ini_Device', name0='Keithley', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
				self.addBoolButton( label='ini_Device', name0='Keithley', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			else:
				self.addLabel(label='ini_Device', name0='Keithley', name1=opt+'(Volt)', frame=self.Device, row=irow, column=icol, sticky='ew')
				self.addOptEntry(label='ini_Device', name0='Keithley', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1

		irow=1
		for opt in self.iniClass.list_Default['LowVoltage']:
			value=self.iniClass.Sections['LowVoltage'][opt]
			self.addLabel(label='ini_Device', name0='LowVoltage', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			self.addBoolButton( label='ini_Device', name0='LowVoltage', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1
	
		irow=1
		for opt in self.iniClass.list_Default['Xray']:
			value=self.iniClass.Sections['Xray'][opt]
			self.addLabel(label='ini_Device', name0='Xray', name1=opt, frame=self.Device, row=irow, column=icol, sticky='ew')
			self.addBoolButton( label='ini_Device', name0='Xray', name1=opt, frame=self.Device, value=value, row=irow+1, column=icol, sticky='ew')
			irow+=2
		icol+=1
		self.expendWindow(self.Device, 5, icol)

		# Pad 
		eliniRow+=1
		self.addXpad( self.ElIni, row=eliniRow)

		### Process = ['Cycle', 'IV', 'Tests', 'OperationDetails']
		eliniRow+=1
		self.Process = Frame( self.ElIni, bg=BG_MASTER, relief=SUNKEN, borderwidth=2)
		self.Process.grid( row=eliniRow, column=1, sticky=N+S+E+W, columnspan=6 )

		eliniRow+=1
		irow=1
		self.addLabel( label='ini_Process', name1='Cycle', frame=self.Process, font=SECTION_FONT, column=0, row=irow )
		icol=1
		self.addEntry(label='ini_Process', name0='Cycle', name1='Other',      frame=self.Process, value='' )
		self.addLabel(label='ini_Process', name0='Cycle', name1='HideOther', frame=self.Process, fg=BG_MASTER)
		for opt in self.iniClass.list_Default['Cycle']:
			value=self.iniClass.Sections['Cycle'][opt]
			if opt == 'nCycles':
				self.addLabel(label='ini_Process', name0='Cycle', name1=opt, frame=self.Process, row=0, column=icol)
				self.addnCycleMenu( label='ini_Process', name0='Cycle', name1=opt, frame=self.Process, value=value, row=irow, column=icol)
			else:
				self.addLabel(label='ini_Process', name0='Cycle', name1=opt+u" (\N{DEGREE SIGN}C)", frame=self.Process,row=0,column=icol)
				self.addOptEntry(label='ini_Process', name0='Cycle', name1=opt, frame=self.Process, value=value, row=irow, column=icol )
			icol+=1
		# spacial iterm for adding new cycles 
		self.Labels['ini_Process_Cycle_HideOther'].grid( row=irow, column=icol)
		self.Entries['ini_Process_Cycle_Other'].grid( row=irow, column=icol)
		self.Entries['ini_Process_Cycle_Other'].bind('<Key>', lambda event:self.chEntryBG(self.Entries['ini_Process_Cycle_Other'], self.lastClickNewCycle))
		self.Entries['ini_Process_Cycle_Other'].bind('<Leave>', lambda event:self.checkChanging(self.Entries['ini_Process_Cycle_Other'],self.lastClickNewCycle ))
		self.Entries['ini_Process_Cycle_Other'].bind('<FocusOut>', lambda event:self.checkChanging(self.Entries['ini_Process_Cycle_Other'],self.lastClickNewCycle ))
		self.Entries['ini_Process_Cycle_Other'].bind('<Return>', lambda event:self.chooseOtherCycle(self.Entries['ini_Process_Cycle_Other']))
		if self.lastClickNewCycle <= 10:
			self.Labels['ini_Process_Cycle_HideOther'].tkraise()
		irow+=2

		self.addLabel( label='ini_Process', name1='IV', frame=self.Process, font=SECTION_FONT, column=0, row=irow )
		icol=1
		for opt in self.iniClass.list_Default['IV']:
			value=self.iniClass.Sections['IV'][opt]
			if opt == 'Delay':
				self.addLabel(label='ini_Process', name0='IV', name1=opt, frame=self.Process, row=irow-1, column=icol)
				self.addDelayMenu( label='ini_Process', name0='IV', name1=opt, frame=self.Process, value=value, row=irow, column=icol)
			else:
				self.addLabel(label='ini_Process', name0='IV', name1=opt+' (Volt)', frame=self.Process, row=irow-1, column=icol)
				self.addOptEntry(label='ini_Process', name0='IV', name1=opt, frame=self.Process, value=value, row=irow, column=icol)
			icol+=1
		irow+=1

		for opt in self.iniClass.list_Default['Tests']:
			self.addLabel(label='ini_Process', name0='Tests', name1=opt, frame=self.Process, row=irow, font=SECTION_FONT)
			value=self.iniClass.Sections['Tests'][opt]
			if opt == 'Test':
				self.addOptEntry(label='ini_Process', name0='Tests', name1=opt, frame=self.Process, value=value, row=irow, column=1, width=20, columnspan=6, isFixed=True)
				irow+=1
				self.addLabel(label='ini_Process', name0='Tests', name1='Options', frame=self.Process, row=irow, rowspan=2, sticky='ns', font=SECTION_FONT)
				self.addTestButton(label='ini_Process', name0='Tests', name1='IV@17', frame=self.Process, row=irow, column=1, sticky='ew')
				self.addTestButton(label='ini_Process', name0='Tests', name1='Pretest@17', frame=self.Process, row=irow, sticky='ew', column=2 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Fulltest@17', frame=self.Process, row=irow, sticky='ew', column=3 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Cycle', frame=self.Process,row=irow,column=4,sticky='nsew', rowspan=2 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Add new test', frame=self.Process,row=irow,column=5, columnspan=2, sticky='we')
				irow+=1
				self.addTestButton(label='ini_Process', name0='Tests', name1='IV@-20', frame=self.Process, row=irow, sticky='ew', column=1 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Pretest@-20', frame=self.Process, row=irow, sticky='ew', column=2 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Fulltest@-20', frame=self.Process, row=irow, sticky='ew', column=3 )
				# spacial iterm for adding new test 
				self.addEntry(label='ini_Process', name0='Tests', name1='NewTest', frame=self.Process, value='Ex: IV@10', row=irow, column=5, sticky='ew', columnspan=2 )
				self.lastClickNewTest='Ex: IV@10'
				self.Entries['ini_Process_Tests_NewTest'].bind('<Key>', lambda event:self.chEntryBG(self.Entries['ini_Process_Tests_NewTest'], self.lastClickNewTest))
				self.Entries['ini_Process_Tests_NewTest'].bind('<Leave>', lambda event:self.checkChanging(self.Entries['ini_Process_Tests_NewTest'],self.lastClickNewTest ))
				self.Entries['ini_Process_Tests_NewTest'].bind('<FocusOut>', lambda event:self.checkChanging(self.Entries['ini_Process_Tests_NewTest'],self.lastClickNewTest ))
				self.Entries['ini_Process_Tests_NewTest'].bind('<Return>', lambda event:self.activeTestButton(self.testButtons["ini_Process_Tests_Add new test"]))

			elif opt == 'TestDescription':
				self.addOptEntry(label='ini_Process', name0='Tests', name1=opt, frame=self.Process, value=value, row=irow, column=1, columnspan=4)
				self.addTestButton(label='ini_Process', name0='Tests', name1='Delete', frame=self.Process, row=irow, column=5 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Clear', frame=self.Process, row=irow, column=6 )
			else:
				self.addOptEntry(label='ini_Process', name0='Tests', name1=opt, frame=self.Process, value=value, row=irow, column=1)
			irow+=1
	
		self.expendWindow(self.Process, irow, 7)

		# Pad 
		eliniRow+=1
		self.addXpad( self.ElIni, row=eliniRow)

		### Operation = ['Hostname', 'TestCenter', 'Operator']
		eliniRow+=1
		self.Operation = Frame( self.ElIni, bg=BG_MASTER)
		self.Operation.grid( row=eliniRow, column=1, sticky=N+S+E+W, columnspan=6 )

		eliniRow+=1
		irow=1
		icol=1
		self.addLabel( label='ini_Operation', name1='OperationDetails', frame=self.Operation, font=SECTION_FONT, column=0, row=irow, sticky='ew' )
		for opt in self.iniClass.list_Default['OperationDetails']:
			value=self.iniClass.Sections['OperationDetails'][opt]
			self.addLabel(label='ini_Operation', name0='OperationDetails', name1=opt, frame=self.Operation, row=irow-1, column=icol, sticky='ew')
			self.addOptEntry(label='ini_Operation', name0='OperationDetails', name1=opt, frame=self.Operation, value=value, row=irow, column=icol, sticky='ew')
			icol+=1
		irow+=1
		self.expendWindow(self.Operation, irow, icol)

		# Pad 
		eliniRow+=1
		self.addXpad( self.ElIni, row=eliniRow)

		eliniRow+=1
		self.expendWindow(self.ElIni, eliniRow, COLUMNMAX)
		### * [END] elComandante_ini * -------------------------------------------------------------------------------------------------------

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
	#app.loadConfig("./elComandante.ini.default")
	app.createWidgets()
	root.mainloop()
