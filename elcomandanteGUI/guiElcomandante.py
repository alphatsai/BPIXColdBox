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
ISINI=1
ISCONF=2
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
TYPING_COLOR='khaki1'
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
		self.lastTestDirEntry={}
		self.lastTestDirMenu={}
		self.hasError=False
		self.Menus={}
		self.Vars={}
		self.configDir = './example'
		self.testDefinePath=''
		self.confingurePath = { 'elComandante.ini' :'./elComandante.ini.default',
								'elComandante.conf':'./elComandante.conf.default' }
		self.confingureOutPut = { 'elComandante.ini' :'./elComandante.ini',
								  'elComandante.conf':'./elComandante.conf' }
		self.whichConfig = { 'elComandante.ini':True,
				     		 'elComandante.conf':False }
		self.currentPath = self.confingurePath['elComandante.ini']
		self.loadElcommandateIni();
		self.loadElcommandateConf();
	
	#### Load configure file
	def loadElcommandateIni(self):
		self.iniClass = elComandante_ini()
		self.iniClass.getDefault(self.confingurePath['elComandante.ini'])
		return

	def loadElcommandateConf(self):
		self.confClass = elComandante_conf()
		self.confClass.getDefault(self.confingurePath['elComandante.conf'])
		return

	def loadTestsOptions(self):
		listDir = commands.getoutput('ls '+self.testDefinePath)
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
				self.currentPath=self.confingurePath[button]
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
					classType = name.split('_')[0]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if classType == 'ini':
						entry.delete(0, END)
						if option == 'Test' and section == 'Tests':
							if not self.checkProcess(self.iniClass.Sections[section][option]):
								entry['bg'] = ERROR_COLOR
						entry.insert(0, self.iniClass.Sections[section][option])
					else:
						continue
				# refresh add new test entry
				self.lastClickNewTest='Ex: IV@10'
				self.Entries['ini_Process_Tests_NewTest'].delete(0,END)
				self.Entries['ini_Process_Tests_NewTest'].insert(0, 'Ex: IV@10')
				# refresh BoolButtons 
				for name in self.BoolButtons:
					button = self.BoolButtons[name]
					classType = name.split('_')[0]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if classType == 'ini':
						self.fillBoolName(button, section, option, self.iniClass.Sections[section][option])
					else:
						continue
				# refresh menu 
				for name in self.Menus:
					menu = self.Menus[name]
					var = self.Vars[name]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if section == 'IV':
						self.setDelayVar( menu, var, section, option, self.iniClass.Sections[section][option])
					elif section == 'Cycle':
						self.setCycleVar( menu, var, section, option, self.iniClass.Sections[section][option])
					elif section == 'ModuleType':
						self.setTypeVar( menu, var, section, option, self.iniClass.Sections[section][option])
				self.currentPath = self.confingurePath['elComandante.ini']
			else:
				print ">> [ERROR] Can't find '%s'"% self.entryConfig.get()
				return
		elif self.whichConfig['elComandante.conf']:
			if os.path.isfile( self.entryConfig.get() ):
				self.confingurePath['elComandante.conf'] = self.entryConfig.get()
				self.loadElcommandateConf()
				# refresh option entries
				for name in self.OptEntries:
					entry = self.OptEntries[name]
					classType = name.split('_')[0]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if classType == 'conf':
						entry.delete(0, END)
						entry.insert(0, self.confClass.Sections[section][option])
					else:
						continue
				# refresh BoolButtons 
				for name in self.BoolButtons:
					button = self.BoolButtons[name]
					classType = name.split('_')[0]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if classType == 'conf':
						self.fillBoolName(button, section, option, self.confClass.Sections[section][option])
					else:
						continue
				# refresh dir menu and entry
				for name in self.Menus:
					menu = self.Menus[name]
					var = self.Vars[name]
					section = name.split('_')[2]
					option = name.split('_')[3]
					if section == 'Directories':
						#self.setDirVar( menu, var, name, self.confClass.Sections[section][option])
						self.setDirVar( var, name, self.confClass.Sections[section][option])
				# check test dir in ini's testButtons
				for tests in ['Fulltest@17','Pretest@17', 'Fulltest@-20', 'Pretest@-20']:
					name = 'ini_Process_Tests_'+tests
					button = self.testButtons[name]
					button['command']=''
					button.unbind('<Button-1>')
					button.unbind('<Leave>')
					if self.checkTests(button, tests):
						button['bg']=FALSE_COLOR
						button['text']=tests
						button['command']=lambda button=button:self.activeTestButton(button)
						button.bind('<Button-1>', lambda event:self.changeColorTestEntry(0))
						button.bind('<Leave>', lambda event:self.changeColorTestEntry(1))

				self.currentPath = self.confingurePath['elComandante.conf']
			else:
				print ">> [ERROR] Can't find '%s'"% self.entryConfig.get()
				return
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
				if self.hasError:
					self.Entries['ini_Process_Tests_Test']['bg']=ERROR_COLOR
		# Locked
		else:
			self.isfixed=True
			self.buttonLock['text']='Unlock'
			self.buttonLock['bg']=UNLOCK_COLOR
			self.locklabel['fg']='red'
			self.entryConfig['bg']=ENTRY_LOCKED_COLOR
			for entry in self.Entries:
				self.Entries[entry]['bg']=ENTRY_LOCKED_COLOR
				if self.hasError:
					self.Entries['ini_Process_Tests_Test']['bg']=ERROR_COLOR
			if int(self.lastClickNewCycle) <= 10:
				self.Labels['ini_Process_Cycle_HideOther'].tkraise()
				self.Vars['ini_Process_Cycle_nCycles'].set(self.lastClickNewCycle)
				self.Menus['ini_Process_Cycle_nCycles']['bg']=MENU_FULL_COLOR
			self.unTouchDir('conf_Directories_Directories_testDefinitions')
			self.unTouchDir('conf_Directories_Directories_dataDir')
	
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
		self.SAVE = Button(frame, font=font, bg=bg, text=text, width=width, fg=TITLE4_COLOR, command= lambda:self.saveConfig() )
		self.SAVE.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

	def saveConfig(self):
		if self.whichConfig['elComandante.ini']:
			self.iniClass.makeConfig(self.confingureOutPut['elComandante.ini'])
		if self.whichConfig['elComandante.conf']:
			self.confClass.makeConfig(self.confingureOutPut['elComandante.conf'])
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
	def addEntry(self, frame, label="", name0="", name1="", value="" , row=0, column=0, width=10, sticky='nsew', columnspan=1, rowspan=1, fg='black' ):
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

		if name1 == 'Test' and name0 == 'Tests':
			if not self.checkProcess(value):
				newEntry['bg'] = ERROR_COLOR
	
		newEntry.insert(0, value)
		newEntry.grid( row=row, column=column, sticky=sticky, columnspan=columnspan, rowspan=rowspan)
		self.Entries[name]=newEntry
		return name

	### Add entry for options from configure file 
	def addOptEntry(self, frame, label="", name0="", name1="", value="" , row=0, column=0, width=10, sticky='nsew', columnspan=1, rowspan=1, isFixed=False, classType=ISINI ):
		name = self.addEntry(frame, label, name0, name1, value, row, column, width, sticky, columnspan, rowspan=rowspan)
		newEntry = self.Entries[name]
		if classType == ISINI:
			if isFixed:
				newEntry.bind('<Key>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1], True))
				newEntry.bind('<Leave>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1]))
				newEntry.bind('<Return>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1], True))
				newEntry.bind('<FocusOut>', lambda event:self.unTouchEntry(newEntry, self.iniClass.Sections[name0][name1]))
			else:
				newEntry.bind('<Key>', lambda event:self.changeEntryBG(newEntry,self.iniClass.Sections[name0][name1] ))
				newEntry.bind('<Leave>', lambda event:self.checkChanging(newEntry, self.iniClass.Sections[name0][name1], name ))
				newEntry.bind('<Return>', lambda event:self.ConfirmChangeOpt(newEntry, name0, name1 ))
				newEntry.bind('<FocusOut>', lambda event:self.checkChanging(newEntry, self.iniClass.Sections[name0][name1],name ))
		if classType == ISCONF:
			if isFixed:
				newEntry.bind('<Key>', lambda event:self.unTouchEntry(newEntry, self.confClass.Sections[name0][name1], True))
				newEntry.bind('<Leave>', lambda event:self.unTouchEntry(newEntry, self.confClass.Sections[name0][name1]))
				newEntry.bind('<Return>', lambda event:self.unTouchEntry(newEntry, self.confClass.Sections[name0][name1], True))
				newEntry.bind('<FocusOut>', lambda event:self.unTouchEntry(newEntry, self.confClass.Sections[name0][name1]))
			else:
				newEntry.bind('<Key>', lambda event:self.changeEntryBG(newEntry,self.confClass.Sections[name0][name1] ))
				newEntry.bind('<Leave>', lambda event:self.checkChanging(newEntry, self.confClass.Sections[name0][name1],name ))
				newEntry.bind('<Return>', lambda event:self.ConfirmChangeOpt(newEntry, name0, name1, ISCONF ))
				newEntry.bind('<FocusOut>', lambda event:self.checkChanging(newEntry, self.confClass.Sections[name0][name1],name ))
		self.Entries[name]=newEntry
		self.OptEntries[name]=newEntry
		return

	def changeEntryBG(self, entry, value, murmur=True):
		if self.isfixed:
			self.unTouchEntry(entry, value, murmur)
			return
		entry['bg']=TYPING_COLOR
		return

	def checkChanging(self, entry, value, name='', murmur=False ):
		if self.isfixed:
			self.unTouchEntry(entry, value, murmur)
			return
		if name == 'ini_Process_Tests_Test':
			if self.hasError:
				return
		if value == entry.get():
			entry['bg']=ENTRY_COLOR

		return

	def ConfirmChangeOpt(self, entry, section, option, classType=ISINI, murmur=True):
		if classType == ISINI:
			value = self.iniClass.Sections[section][option]
		if classType == ISCONF:
			value = self.confClass.Sections[section][option]

		if self.isfixed:
			self.unTouchEntry(entry, value, murmur)
			return

		newvalue = entry.get().strip()
		if value != newvalue and newvalue !='':
			print ">> [INFO] Change %s : %s : %s -> %s "%(section, option, value, newvalue)
			if classType == ISINI:
				self.iniClass.changeOptValue(section,option, newvalue)
			if classType == ISCONF:
				self.confClass.changeOptValue(section,option, newvalue)
			entry['bg']=ENTRY_COLOR
		return

	def unTouchEntry(self, entry, value, murmur=False ):
		if murmur:
			print '>> [INFO] The entry is locked!'
		entry.delete(0, END)
		entry.insert(0, value)
		return	

	def checkProcess(self, process):
		newProcess = ''
		size = len(process.split(','))
		i=1
		error=False
		for tests in process.split(','):
			test = tests.split('@')[0]
			if test not in self.tests and test != 'IV' and test != 'Cycle':
				print ">> [ERROR] Can't find '"+test+"' in '"+self.testDefinePath+"'"
				print ">>         Please check the test name"
				error=True
		if not error:
			self.hasError=False
			return True
		else:
			self.hasError=True
			return False

	### Add button for bool options from configure file 
	def addBoolButton(self, frame, label="", name0="", name1="", row=0, column=0, columnspan=1, value='', sticky='wn', width=5, classType=ISINI):
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
		newButton['command']=lambda:self.changeBool( name, name0, name1, classType )
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

	def changeBool(self, name, section, option, classType=ISINI):
		if self.isfixed:
			print '>> [INFO] The button is locked!'
			return
			
		if self.BoolButtons[name]['text'] == "OFF":
			print ">> [INFO] Change %s : %s : False -> True "%(section, option)
			self.BoolButtons[name]['text']="ON"
			self.BoolButtons[name]['bg']=TRUE_COLOR
			if classType == ISINI:
				self.iniClass.changeOptValue(section,option,"True")
			if classType == ISCONF:
				self.confClass.changeOptValue(section,option,"True")
		else:
			print ">> [INFO] Change %s : %s : %s -> False "%(section, option, self.BoolButtons[name]['text'] )
			self.BoolButtons[name]['text']="OFF"
			self.BoolButtons[name]['bg']=FALSE_COLOR
			if classType == ISINI:
				self.iniClass.changeOptValue(section,option,"False")
			if classType == ISCONF:
				self.confClass.changeOptValue(section,option,"False")
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
		testfile =  self.testDefinePath+'/'+test
		if test=='IV' or test== 'Cycle' or test=='Add new test' or test=='Delete' or test=='Clear':
			return True
		elif not os.path.isfile(testfile):
			print ">> [ERROR] Can't find '"+test+"' in '"+self.testDefinePath+"', or it's not a file..."
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
			self.hasError=False
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
			if not self.checkProcess(restTests):
				self.Entries['ini_Process_Tests_Test']['bg'] = ERROR_COLOR
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
					if not self.checkProcess(tests):
						self.Entries['ini_Process_Tests_Test']['bg'] = ERROR_COLOR
					return
				elif len(newtests) == 2:
					temperature = newtests[1]
					if not temperature.isdigit():
						self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
						print '>> [ERROR] After @ shall be digit, i.e temperature'
						print '>>         E.x: Fulltest@17'
						self.lastClickNewTest=''
						if not self.checkProcess(tests):
							self.Entries['ini_Process_Tests_Test']['bg'] = ERROR_COLOR
						return

				if newtest in self.tests or newtest == 'IV' or newtest == 'Cycle':
					if newtest == 'Cycle' and len(newtests)!=1:
						self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
						print ">> [ERROR] Cycle shall not add @ and temperature"
						self.lastClickNewTest=''
						if not self.checkProcess(tests):
							self.Entries['ini_Process_Tests_Test']['bg'] = ERROR_COLOR
						return
					
					if len(newalltests) > 1 and i<len(newalltests):
						newprocess += newTests.strip()+','
					else:
						newprocess += newTests.strip()
					i+=1
					self.Entries['ini_Process_Tests_NewTest']['bg']=ENTRY_COLOR
				else:
					self.Entries['ini_Process_Tests_NewTest']['bg']=ERROR_COLOR
					print ">> [ERROR] Not found '"+newtest+"' in "+self.testDefinePath
					print ">>         Please add it in '"+self.testDefinePath+"' and reload"
					self.lastClickNewTest=''
					if not self.checkProcess(tests):
						self.Entries['ini_Process_Tests_Test']['bg'] = ERROR_COLOR
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
		if not self.checkProcess(tests):
			self.Entries['ini_Process_Tests_Test']['bg'] = ERROR_COLOR
		return
	
	def changeColorTestEntry(self, action):
		if self.isfixed:
			return

		if action == 0: #<Button-1>
			self.Entries['ini_Process_Tests_Test']['bg']=TYPING_COLOR
		elif action == 1: #<Leave>
			if not self.hasError:
				self.Entries['ini_Process_Tests_Test']['bg']=ENTRY_COLOR
			else:
				return
		
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
		self.Menus[name]=newMenu
		self.Vars[name]=var
	
	def setDelayVar(self, menu, var, section, option, value):
		menu['bg'] = ERROR_COLOR
		menu['fg']=TITLE4_COLOR
		menu['font']=BUTTON_FONT
		try:
			fvalue = float(value)
			menu['bg'] = MENU_FULL_COLOR
			var.set(str(int(fvalue*2))+' Sec.')
		except:
			print ">> [ERROR] "+section+" '"+option+"' has wrong value '"+value+"'"
			print ">>         Please select the number to fix it" 
			var.set("ERROR")
				
	def chooseDelay(self, menu, sec, section, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return

		value = self.iniClass.Sections[section][option]
		if float(value)*2 != sec:
			print ">> [INFO] Change %s : %s : %s(%2.0f sec) -> %s(%2.0f sec) "%(section, option, value, float(value)*2, str(sec/2), sec)
			menu['bg'] = MENU_FULL_COLOR
			var.set(str(int(sec))+' Sec.')
			self.iniClass.changeOptValue(section,option, str(sec/2))
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
		self.Menus[name]=newMenu
		self.Vars[name]=var

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

	def chooseCycle(self, menu, label, section, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return
		value = self.iniClass.Sections[section][option]
		if value != label:
			var.set(label)
			if label == 'Other':
				menu['bg'] = FALSE_COLOR
				self.Entries['ini_Process_Cycle_Other'].tkraise()
			else:
				print ">> [INFO] Change %s : %s : %s -> %s "%(section, option, value, label)
				menu['bg'] = MENU_FULL_COLOR
				self.iniClass.changeOptValue(section,option,label)
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

			self.lastClickNewCycle=newvalue

			if int(newvalue) <= 10:
				self.Labels['ini_Process_Cycle_HideOther'].tkraise()
				self.Entries['ini_Process_Cycle_Other'].delete(0, END)
				self.Entries['ini_Process_Cycle_Other']['bg']=ENTRY_COLOR
				self.Vars['ini_Process_Cycle_nCycles'].set(self.lastClickNewCycle)
				self.Menus['ini_Process_Cycle_nCycles']['bg']=MENU_FULL_COLOR
				
			print ">> [INFO] Change Cycle : nCycles : %s -> %s "%( value, newvalue)
			self.iniClass.changeOptValue('Cycle', 'nCycles', newvalue)
			entry['bg']=ENTRY_COLOR
		return

	def checkEmpty(self, entry):
		if entry.get() == '' or int(entry.get()) <= 10:
				self.Labels['ini_Process_Cycle_HideOther'].tkraise()
				self.Entries['ini_Process_Cycle_Other'].delete(0, END)
				self.Entries['ini_Process_Cycle_Other']['bg']=ENTRY_COLOR
				self.Vars['ini_Process_Cycle_nCycles'].set(self.lastClickNewCycle)
				self.Menus['ini_Process_Cycle_nCycles']['bg']=MENU_FULL_COLOR
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
		self.Menus[name]=newMenu
		self.Vars[name]=var
	
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

	def chooseType(self, menu, label, section, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return
		value = self.iniClass.Sections[section][option]
		if value != label:
			print ">> [INFO] Change %s : %s : %s -> %s "%(section, option, value, label)
			if label == 'Full':
				menu['bg'] = MENU_FULL_COLOR
			if label == 'Roc':
				menu['bg'] = MENU_ROC_COLOR
			var.set(label)
			self.iniClass.changeOptValue(section,option,label)
		return

	### Add Menu for testDefinetions from configure file 
	def addTestDirMenu(self, frame, label="", name0="", name1="", row=0, column=0, columnspan=1, value='', sticky='wn', width=5):
		term1=""
		term2=""
		if label!="" :
			term1=label+"_"
		if name0!="" :
			term2=name0+"_"
		name=term1+term2+name1

		var=StringVar()
		newMenu = OptionMenu( frame, var, () )

		self.Menus[name]=newMenu
		self.Vars[name]=var

		newMenu['width'] = width
		newMenu['menu'].delete(0)
		if name1 == 'testDefinitions':	
			newMenu['menu'].add_command( label="$configDir", command=lambda:self.chooseTestDir( newMenu, '$configDir', name, name0, name1, var))
			newMenu['menu'].add_command( label="Other",  command=lambda:self.chooseTestDir( newMenu, 'Other', name, name0, name1, var,))
		if name1 == 'dataDir':
			newMenu['menu'].add_command( label="$baseDir", command=lambda:self.chooseTestDir( newMenu, '$baseDir', name, name0, name1, var))
			newMenu['menu'].add_command( label="Other",  command=lambda:self.chooseTestDir( newMenu, 'Other', name, name0, name1, var,))
	
		newMenu.grid( row=row, column=column, sticky=sticky, columnspan=columnspan)
		self.setDirVar( var, name, value)
	
	def setDirVar(self, var, name, value):
		menu = self.Menus[name]
		menu['bg'] = ERROR_COLOR
		menu['fg']=TITLE4_COLOR
		menu['font']=BUTTON_FONT
		terms = value.strip().split('/')
		option = name.split('_')[3]
		if terms[0]=='$configDir$':
			menu['bg'] = MENU_FULL_COLOR
			var.set('$configDir')
			entry=''
			for term in terms:
				if term != '$configDir$':
					entry+='/'+term
			self.Entries[name].delete(0, END)
			self.Entries[name].insert(0, entry)
			self.lastTestDirEntry[name]=entry
			self.lastTestDirMenu[name]='$configDir'
			self.testDefinePath = self.configDir+entry
			self.loadTestsOptions()
		elif terms[0]=='<!Directories|baseDir!>':
			menu['bg'] = MENU_FULL_COLOR
			var.set('$baseDir')
			entry=''
			for term in terms:
				if term != '<!Directories|baseDir!>':
					entry+='/'+term
			self.Entries[name].delete(0, END)
			self.Entries[name].insert(0, entry)
			self.lastTestDirEntry[name]=entry
			self.lastTestDirMenu[name]='$baseDir'
		else:
			menu['bg'] = FALSE_COLOR
			var.set('Other')
			self.Entries[name].delete(0, END)
			self.Entries[name].insert(0, value)
			self.lastTestDirEntry[name]=value
			self.lastTestDirMenu[name]='Other'
			if option == 'testDefinitions':
				self.testDefinePath = value 
				self.loadTestsOptions()
		return

	def chooseTestDir(self, menu, label, name, section, option, var):
		if self.isfixed:
			print '>> [INFO] The menu is locked!'
			return

		self.Entries[name]['bg']=TYPING_COLOR
		menu['bg'] = TYPING_COLOR
		var.set(label)
		return
			 
	def unTouchDir(self, name, murmur=False ):
		if murmur:
			print '>> [INFO] The all dir is locked!'

		menu = self.Menus[name]
		var = self.Vars[name]
		var.set(self.lastTestDirMenu[name])
		if var.get() == 'Other':
			menu['bg']=FALSE_COLOR
		else:
			menu['bg']=MENU_FULL_COLOR
		entry = self.Entries[name]
		entry.delete(0, END)
		entry.insert(0, self.lastTestDirEntry[name])
		return
	
	def changeDirBG(self, name, murmur=True):
		if self.isfixed:
			self.unTouchDir(name, murmur)
			return
		menu = self.Menus[name]
		entry = self.Entries[name]
		menu['bg']=TYPING_COLOR
		entry['bg']=TYPING_COLOR
		return

	def checkDirChanging(self, name, murmur=False):
		if self.isfixed:
			self.unTouchDir(name, murmur)
			return
		entry = self.Entries[name]
		menu = self.Menus[name]
		var = self.Vars[name]
		if self.lastTestDirMenu[name] == var.get() and self.lastTestDirEntry[name] == entry.get():
			entry['bg']=ENTRY_COLOR
			if var.get() == 'Other':
				menu['bg'] = FALSE_COLOR
			else:	
				menu['bg'] = MENU_FULL_COLOR
		return

	def confirmTestDir(self, name, murmur=True ):
			if self.isfixed:
				self.unTouchDir(name, murmur)
				return
			section = name.split('_')[2]
			option = name.split('_')[3]
			value = self.confClass.Sections[section][option]
			entry = self.Entries[name]
			menu = self.Menus[name]
			var = self.Vars[name]
			newvalue = '' 
			if var.get() == '$configDir':
				newvalue = '$configDir$'+entry.get()
				if option == 'testDefinitions':
					self.testDefinePath = self.configDir+entry.get()
					self.loadTestsOptions()
			elif var.get() == '$baseDir':
				newvalue = '<!Directories|baseDir!>'+entry.get()
			else:
				newvalue = entry.get()
				if option == 'testDefinitions':
					self.testDefinePath = entry.get() 
					self.loadTestsOptions()

			self.lastTestDirEntry[name]=entry.get()
			self.lastTestDirMenu[name]=var.get()
			if value != newvalue:
				print ">> [INFO] Change %s : %s : %s -> %s "%(section, option, value, newvalue)
				entry['bg']=ENTRY_COLOR
				self.confClass.changeOptValue(section,option,newvalue)
				if self.lastTestDirMenu[name] != 'Other':
					menu['bg']=MENU_FULL_COLOR
				else:
					menu['bg']=FALSE_COLOR
			else:
				if self.lastTestDirMenu[name] != 'Other':
					menu['bg']=MENU_FULL_COLOR
				else:
					menu['bg']=FALSE_COLOR
				entry['bg']=ENTRY_COLOR
				return
			
			if option == 'testDefinitions':
				for tests in ['Fulltest@17','Pretest@17', 'Fulltest@-20', 'Pretest@-20']:
					name = 'ini_Process_Tests_'+tests
					button = self.testButtons[name]
					button['command']=''
					button.unbind('<Button-1>')
					button.unbind('<Leave>')
					if self.checkTests(button, tests):
						button['bg']=FALSE_COLOR
						button['text']=tests
						button['command']=lambda button=button:self.activeTestButton(button)
						button.bind('<Button-1>', lambda event:self.changeColorTestEntry(0))
						button.bind('<Leave>', lambda event:self.changeColorTestEntry(1))
			return

	######## * Main function and platform ####### ======================================================================================
	def createWidgets(self):
		### * Plot * -------------------------------------------------------------------------------------------------------
		#t = Toplevel(self.master)
		#t.wm_title("Plot" )
		#l = Label(t, text="This is Plot")
		#l.pack(side="top", fill="both", expand=True, padx=100, pady=100)


		### [END] Plot * ---------------------------------------------------------------------------------------------------

		# Pad 
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
		self.entryConfig.bind('<Key>', lambda event:self.changeEntryBG(self.entryConfig, self.currentPath ))
		self.entryConfig.bind('<Leave>', lambda event:self.checkChanging(self.entryConfig, self.currentPath ))
		self.entryConfig.bind('<FocusOut>', lambda event:self.checkChanging(self.entryConfig, self.currentPath ))

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

		### * elComandante_conf * -------------------------------------------------------------------------------------------------------
		### DTBAddress = ['TB0', 'TB1', 'TB2', 'TB3']
		# Pad 
		elconfRow=0
		self.addXpad( self.ElConf, row=elconfRow)

		elconfRow+=1
		self.DTBAddress = Frame( self.ElConf, bg=BG_MASTER, relief=RAISED, borderwidth=2)
		self.DTBAddress.grid( row=elconfRow, column=1, sticky=N+S+E+W, columnspan=6 )

		irow=1
		icol=1
		self.addLabel( label='conf_DTB', name1='TestboardAddress', frame=self.DTBAddress, font=SECTION_FONT, column=0, row=irow, sticky='ew' )
		for opt in self.confClass.list_Default['TestboardAddress']:
			value=self.confClass.Sections['TestboardAddress'][opt]
			self.addLabel(label='conf_DTB', name0='TestboardAddress', name1=opt, frame=self.DTBAddress, row=irow-1, column=icol, sticky='ew', columnspan=1)
			self.addOptEntry(label='conf_DTB', name0='TestboardAddress', name1=opt, frame=self.DTBAddress, value=value, row=irow, column=icol, sticky='ew', columnspan=1, classType=ISCONF, width=15)
			icol+=1
		irow+=1
		self.expendWindow(self.DTBAddress, irow, icol)

		### Subsysterm = ['subsystem', 'jumoClient', 'keithleyClient', 'psiClient']
		elconfRow+=1
		self.addXpad( self.ElConf, row=elconfRow)

		elconfRow+=1
		self.Subsysterm = Frame( self.ElConf, bg=BG_MASTER, relief=RAISED, borderwidth=2)
		self.Subsysterm.grid( row=elconfRow, column=1, sticky=N+S+E+W, columnspan=6 )

		irow
		icol=1
		self.addLabel( label='conf_Subsysterm', name1='subsystem', frame=self.Subsysterm, font=SECTION_FONT, column=0, row=1, sticky='ew' )
		for opt in self.confClass.list_Default['subsystem']:
			if opt != 'Ziel' and opt != 'Port':
				continue
			value=self.confClass.Sections['subsystem'][opt]
			self.addLabel(label='conf_Subsysterm', name0='subsystem', name1=opt, frame=self.Subsysterm, row=0, column=icol, sticky='ew')
			self.addOptEntry(label='conf_Subsysterm', name0='subsystem', name1=opt, frame=self.Subsysterm, value=value, row=1, column=icol, sticky='ew', classType=ISCONF)
			icol+=1

		startCol=1
		irow=4
		icol=startCol
		self.addLabel( label='conf_Subsysterm', name1='Clients', frame=self.Subsysterm, font=SECTION_FONT, column=0, row=irow-1, sticky='ew' )
		self.addLabel( label='conf_Subsysterm', name1='jumoClient',   frame=self.Subsysterm, font=SECTION_FONT, column=startCol, row=irow-2, sticky='ew' )
		self.addLabel( label='conf_Subsysterm', name1='keithleyClient', frame=self.Subsysterm, font=SECTION_FONT, column=startCol+1, row=irow-2, sticky='ew' )
		self.addLabel( label='conf_Subsysterm', name1='psiClient',       frame=self.Subsysterm, font=SECTION_FONT, column=startCol+2, row=irow-2, sticky='ew', columnspan=3 )
		for opt in self.confClass.list_Default['jumoClient']:
			if opt != 'port':
				continue
			value=self.confClass.Sections['jumoClient'][opt]
			self.addLabel(label='conf_Subsysterm', name0='jumoClient', name1=opt, frame=self.Subsysterm, row=irow-1, column=icol, sticky='ew')
			self.addOptEntry(label='conf_Subsysterm', name0='jumoClient', name1=opt, frame=self.Subsysterm, value=value, row=irow, column=icol, sticky='ew', classType=ISCONF)
			irow+=2
		icol+=1

		irow=4
		for opt in self.confClass.list_Default['keithleyClient']:
			if opt != 'port':
				continue
			value=self.confClass.Sections['keithleyClient'][opt]
			self.addLabel(label='conf_Subsysterm', name0='keithleyClient', name1=opt, frame=self.Subsysterm, row=irow-1, column=icol, sticky='ew')
			self.addOptEntry(label='conf_Subsysterm', name0='keithleyClient', name1=opt, frame=self.Subsysterm, value=value, row=irow, column=icol, sticky='ew', classType=ISCONF)
			irow+=2
		icol+=1
	
		irow=4
		for opt in self.confClass.list_Default['psiClient']:
			value=self.confClass.Sections['psiClient'][opt]
			self.addLabel(label='conf_Subsysterm', name0='psiClient', name1=opt, frame=self.Subsysterm, row=irow-1, column=icol, sticky='ew', columnspan=3)
			self.addOptEntry(label='conf_Subsysterm', name0='psiClient', name1=opt, frame=self.Subsysterm, value=value, row=irow, column=icol, sticky='ew', classType=ISCONF, columnspan=3)
			irow+=2
		icol+=3
		self.expendWindow(self.Subsysterm, 6, icol)

		### Directories = ['testDefinitions', 'dataDir', 'defaultParameters' ] and defaultParameters = [Full, Roc]
		elconfRow+=1
		self.addXpad( self.ElConf, row=elconfRow)

		elconfRow+=1
		self.Directories = Frame( self.ElConf, bg=BG_MASTER, relief=RAISED, borderwidth=2)
		self.Directories.grid( row=elconfRow, column=1, sticky=N+S+E+W, columnspan=6 )

		self.addLabel( label='conf_Directories', name1='Directories', frame=self.Directories, font=SECTION_FONT, column=0, row=1, sticky='ew' )
		self.addLabel( label='conf_Directories', name1='defaultParameters', frame=self.Directories, font=SECTION_FONT, column=0, row=2, sticky='nsew', rowspan=2 )
		self.addLabel( label='conf_Directories', name0='defaultParameters', name1='Full', frame=self.Directories, font=SECTION_FONT, column=3, row=2, sticky='ew', bg=MENU_FULL_COLOR )
		self.addLabel( label='conf_Directories', name0='defaultParameters', name1='Roc', frame=self.Directories, font=SECTION_FONT, column=3, row=3, sticky='ew', bg=MENU_ROC_COLOR  )

		value = self.confClass.Sections['Directories']['defaultParameters']
		self.addOptEntry(label='conf_Directories', name0='Directories', name1='defaultParameters', frame=self.Directories, value=value, row=2, column=1, sticky='nsew', rowspan=2, columnspan=2, classType=ISCONF)
		value = self.confClass.Sections['defaultParameters']['Full']
		self.addOptEntry(label='conf_Directories', name0='defaultParameters', name1='Full', frame=self.Directories, value=value, row=2, column=4, sticky='ew', classType=ISCONF, width=15)
		value = self.confClass.Sections['defaultParameters']['Roc']
		self.addOptEntry(label='conf_Directories', name0='defaultParameters', name1='Roc', frame=self.Directories, value=value, row=3, column=4, sticky='ew', classType=ISCONF)

		value = self.confClass.Sections['Directories']['testDefinitions']
		self.addLabel(label='conf_Directories', name0='Directories', name1='testDefinitions', frame=self.Directories, row=0, column=1, sticky='ew', columnspan=2)
		self.addEntry(label='conf_Directories', name0='Directories', name1='testDefinitions', frame=self.Directories, value='', row=1, column=2, sticky='ew')
		self.addTestDirMenu( label='conf_Directories', name0='Directories', name1='testDefinitions', frame=self.Directories, value=value, row=1, column=1, sticky='ew')
		self.Entries['conf_Directories_Directories_testDefinitions'].bind('<Key>', lambda event:self.changeDirBG('conf_Directories_Directories_testDefinitions'))
		self.Entries['conf_Directories_Directories_testDefinitions'].bind('<Leave>', lambda event:self.checkDirChanging('conf_Directories_Directories_testDefinitions'))
		self.Entries['conf_Directories_Directories_testDefinitions'].bind('<FocusOut>', lambda event:self.checkDirChanging('conf_Directories_Directories_testDefinitions'))
		self.Entries['conf_Directories_Directories_testDefinitions'].bind('<Return>', lambda event:self.confirmTestDir('conf_Directories_Directories_testDefinitions'))
		self.Menus['conf_Directories_Directories_testDefinitions'].bind('<Leave>', lambda event:self.checkDirChanging('conf_Directories_Directories_testDefinitions'))

		value = self.confClass.Sections['Directories']['dataDir']
		self.addLabel(label='conf_Directories', name0='Directories', name1='dataDir', frame=self.Directories, row=0, column=3, sticky='ew', columnspan=2)
		self.addEntry(label='conf_Directories', name0='Directories', name1='dataDir', frame=self.Directories, value='', row=1, column=4, sticky='ew', width=15)
		self.addTestDirMenu( label='conf_Directories', name0='Directories', name1='dataDir', frame=self.Directories, value=value, row=1, column=3, sticky='ew')
		self.Entries['conf_Directories_Directories_dataDir'].bind('<Key>', lambda event:self.changeDirBG('conf_Directories_Directories_dataDir'))
		self.Entries['conf_Directories_Directories_dataDir'].bind('<Leave>', lambda event:self.checkDirChanging('conf_Directories_Directories_dataDir'))
		self.Entries['conf_Directories_Directories_dataDir'].bind('<FocusOut>', lambda event:self.checkDirChanging('conf_Directories_Directories_dataDir'))
		self.Entries['conf_Directories_Directories_dataDir'].bind('<Return>', lambda event:self.confirmTestDir('conf_Directories_Directories_dataDir'))
		self.Menus['conf_Directories_Directories_dataDir'].bind('<Leave>', lambda event:self.checkDirChanging('conf_Directories_Directories_dataDir'))

		self.expendWindow(self.Directories, 5, 5)

		### Transfer = ['host', 'port', 'destination', 'user', 'checkFortar']
		elconfRow+=1
		self.addXpad( self.ElConf, row=elconfRow)

		elconfRow+=1
		self.Transfer = Frame( self.ElConf, bg=BG_MASTER, relief=RAISED, borderwidth=2)
		self.Transfer.grid( row=elconfRow, column=1, sticky=N+S+E+W, columnspan=6 )

		irow=1
		icol=1
		self.addLabel( label='conf_Transfer', name1='Transfer', frame=self.Transfer, font=SECTION_FONT, column=0, row=irow, sticky='ew' )
		self.addLabel( label='conf_Transfer', name1='HideForAlignment', frame=self.Transfer, font=SECTION_FONT, column=0, row=irow+2, sticky='ew', fg=BG_MASTER)
		for opt in self.confClass.list_Default['Transfer']:
			value=self.confClass.Sections['Transfer'][opt]
			if opt == 'checkForTars':
				self.addLabel(label='conf_Transfer', name0='Transfer', name1=opt, frame=self.Transfer, row=irow+1, column=1, sticky='ew', columnspan=1)
				self.addBoolButton( label='conf_Transfer', name0='Transfer', name1=opt, frame=self.Transfer, value=value, row=irow+2, column=1, sticky='ew', classType=ISCONF, columnspan=1)
				icol+=1
			else:
				self.addLabel(label='conf_Transfer', name0='Transfer', name1=opt, frame=self.Transfer, row=irow-1, column=icol, sticky='ew', columnspan=1)
				self.addOptEntry(label='conf_Transfer', name0='Transfer', name1=opt, frame=self.Transfer, value=value, row=irow, column=icol, sticky='ew', columnspan=1, classType=ISCONF, width=15)
				icol+=1
		irow+=1
		self.expendWindow(self.Transfer, 5, icol-1)

		# Pad 
		elconfRow+=1
		self.addXpad( self.ElConf, row=elconfRow)

		elconfRow+=1
		self.expendWindow(self.ElConf, elconfRow, COLUMNMAX)

		### * [END] elComandante_conf * -------------------------------------------------------------------------------------------------------


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
		self.addLabel( label='ini_Device', name1='Keithley',   frame=self.Device, font=SECTION_FONT, column=startCol+1, row=0, sticky='ew' )
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
		self.Entries['ini_Process_Cycle_Other'].bind('<Key>', lambda event:self.changeEntryBG(self.Entries['ini_Process_Cycle_Other'], self.lastClickNewCycle))
		self.Entries['ini_Process_Cycle_Other'].bind('<Leave>', lambda event:self.checkChanging(self.Entries['ini_Process_Cycle_Other'],self.lastClickNewCycle ))
		self.Entries['ini_Process_Cycle_Other'].bind('<FocusOut>', lambda event:self.checkChanging(self.Entries['ini_Process_Cycle_Other'],self.lastClickNewCycle ))
		self.Entries['ini_Process_Cycle_Other'].bind('<FocusOut>', lambda event:self.checkEmpty(self.Entries['ini_Process_Cycle_Other']))
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
				self.addTestButton(label='ini_Process', name0='Tests', name1='Fulltest@17', frame=self.Process, row=irow, sticky='ew', column=2 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Pretest@17', frame=self.Process, row=irow, sticky='ew', column=3 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Cycle', frame=self.Process,row=irow,column=4,sticky='nsew', rowspan=2 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Add new test', frame=self.Process,row=irow,column=5, columnspan=2, sticky='we')
				irow+=1
				self.addTestButton(label='ini_Process', name0='Tests', name1='IV@-20', frame=self.Process, row=irow, sticky='ew', column=1 )
				self.addTestButton(label='ini_Process', name0='Tests', name1='Fulltest@-20', frame=self.Process, row=irow, sticky='ew', column=2)
				self.addTestButton(label='ini_Process', name0='Tests', name1='Pretest@-20', frame=self.Process, row=irow, sticky='ew', column=3 )
				# spacial iterm for adding new test 
				self.addEntry(label='ini_Process', name0='Tests', name1='NewTest', frame=self.Process, value='Ex: IV@10', row=irow, column=5, sticky='ew', columnspan=2 )
				self.lastClickNewTest='Ex: IV@10'
				self.Entries['ini_Process_Tests_NewTest'].bind('<Key>', lambda event:self.changeEntryBG(self.Entries['ini_Process_Tests_NewTest'], self.lastClickNewTest))
				self.Entries['ini_Process_Tests_NewTest'].bind('<Leave>', lambda event:self.checkChanging(self.Entries['ini_Process_Tests_NewTest'],self.lastClickNewTest, 'ini_Process_Tests_NewTest' ))
				self.Entries['ini_Process_Tests_NewTest'].bind('<FocusOut>', lambda event:self.checkChanging(self.Entries['ini_Process_Tests_NewTest'],self.lastClickNewTest, 'ini_Process_Tests_NewTest' ))
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
			self.addOptEntry(label='ini_Operation', name0='OperationDetails', name1=opt, frame=self.Operation, value=value, row=irow, column=icol, sticky='ew', width=15)
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
	app.createWidgets()
	root.mainloop()

