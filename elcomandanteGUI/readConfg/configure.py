#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from ConfigParser import *

class configure:

	def __init__(self, debug=False):
		self.className = "configure"
		self.defaultOutput = "config"
		self.defaultConf = ""
		self.parser = SafeConfigParser()
		self.parser.optionxform = str
		self.hasDefault = False
		self.debug = debug	

		# list: Pars list -  can be customily extended by fuctions 
		self.list_Sections = [
			# section_name,
		]

		# dict: Default sections and options in configure file
		self.list_Default = {
			# section_name:["option1", "option2", ...],
		}

		# dict: Pars map - default containor
		self.Sections = {
			# section_name:{"option1":"value1", "option2":"value2", ... },
		}

	def loadDefault( self, configFile="" ):
		self.defaultConf = configFile
		if not os.path.isfile(self.defaultConf):
			print ">> [ERROR] Can't find '"+self.defaultConf+"', or it's not a file..."
		else: 
			self.parser.read(self.defaultConf)
			self.hasDefault = True 
			print '>> [INFO] Loaded %s...' %self.defaultConf
		return

	# It will load default sections and options from configure file default structure,
	# If you want use new section and options in configure file, then "addNewSection" has to be "True"
	def getDefault(self, configFile, addNewSection=False ):
		self.loadDefault(configFile)
		print '>> [INFO] Checking default parameter...' 
		for defaultSection in self.list_Default:
			if not self.parser.has_section(defaultSection):
				print ">> [ERROR] No default section: '"+defaultSection+"' in "+configFile
				print ">>         Teminated %s::getDefault()" % self.className
				return
			else:
				for defaultOpt in self.list_Default[defaultSection]:
					if not self.parser.has_option( defaultSection, defaultOpt): 
						print ">> [ERROR] No default option: '"+defaultOpt+"' under "+defaultSection+" in "+configFile
						print ">>         Teminated %s::getDefault()"% self.className
						return
		print '>> [INFO] Filling parameters...'
		for loadSection in self.parser.sections():
			if loadSection in self.list_Default:
				for loadOpt in self.parser.options(loadSection):
					self.Sections[loadSection][loadOpt]=self.parser.get(loadSection, loadOpt)
					if self.debug: 
						print ">> [DEBUG] Got default {0:<15s} option: {1:<25s}".format("'"+loadSection+"'", loadOpt)
			else: 	
				if addNewSection:
					self.makeNewSection(loadSection)
					for loadOpt in self.parser.options(loadSection):
						self.makeNewOption( loadSection, loadOpt, self.parser.get(loadSection, loadOpt))
						if self.debug: 
							print ">> [DEBUG] Got default {0:<15s} option: {1:<25s}".format("'"+loadSection+"'", loadOpt)
		print '>> [INFO] Done!'
		return

	def listSections(self):
		print ">> [INFO] Call %s::listSections()"% self.className	
		print ">>        Sections: "
		for sec in self.list_Sections:
			print ">>                  "+sec
		return
	
	def makeNewSection(self, newSec ):
		if self.debug:  
			print ">> [DEBUG] Call %s::makeNewSection( newSec, newOpts  )"% self.className	
			print ">>         newSec: "+newSec	
			#print ">>         newOpts: "+str(newOpts)
		if newSec in self.Sections:
			print ">> [ERROR] Section "+newSec+" existed"
			return
		else:
			self.list_Sections.append(newSec)
			self.Sections[newSec]={}
		return

	def makeNewOption(self, secName="", newOptsName="", newValue="" ):
		if self.debug:  
			print ">> [DEBUG] Call %s::makeNewOption( secName, newOptsName, newValue  )"% self.className	
			print ">>         secName:     "+secName	
			print ">>         newOptsName: "+newOptsName
			print ">>         newValue:    "+newValue
		if secName in self.Sections:
			if newOptsName in self.Sections[secName]:
				print ">> [ERROR] Option "+newOptsName+" existed in "+secName
				return
			else:
				self.Sections[secName][newOptsName]=newValue
		else:
			print ">> [ERROR] Not found section "+secName
		return
		
	def changeOptValue(self, secName="", optName="", newValue="" ):
		if self.debug:  
			print ">> [DEBUG] Call %s::changeOptValue( secName, optName, newValue  )"% self.className	
			print ">>         secName:  "+secName	
			print ">>         optName:  "+optName
			print ">>         newValue: "+newValue
		if secName in self.Sections:
			if optName in self.Sections[secName]:
				self.Sections[secName][optName]=newValue
			else:
				print ">> [ERROR] Not found option "+optName+" in "+secName
		else:
			print ">> [ERROR] Not found section "+secName
		return

	def listOptions(self, secName=None ):
		if secName in self.Sections:
			print ">> [INFO] Call %s::listOptions( %s )"%( self.className, secName )
			print ">>        Options: "
			for opt in self.Sections[secName]:
				print ">>                "+opt
		else:
			print ">> [INFO] Call %s::listOptions( secName )"% self.className 
			print ">> [ERROR] Not found section "+secName
		return

	def callOption(self, secName=None, optName=None ):
		if secName == None or optName == None:
			print ">> [ERROR] No input in %s::callOption( secName, optName )"% self.className 
			return	
		if secName in self.Sections:
			if optName in self.Sections[secName]:
				print ">> [INFO] Call %s::callOption( %s, %s )"%( self.className, secName, optName )
				print ">>        Value: "+self.Sections[secName][optName]
			else:
				print ">> [INFO] Call %s::callOption( secName, optName )"% self.className 
				print ">> [ERROR] Not found option "+optName+" in "+secName
		else:
			print ">> [INFO] Call %s::callOption( %s, %s )"%( self.className, secName, optName )
			print ">> [ERROR] Not found section "+secName
		return

	def callConfig(self):
		print ">> [INFO] Print out current configure"
		print ">> ================== Current %s =================\n"% self.defaultOutput
		for section in self.list_Sections:
			print " ["+section+"]"
			for opt in sorted(self.Sections[section]):
				print " "+opt+" : "+self.Sections[section][opt]
			print ""
		print ">> ======================================================"
		print ">> [INFO] DONE!"
		return

	def makeConfig( self, outFile=None ):
		if outFile == None:
			outFile=self.defaultOutput	
		print ">> [INFO] Writing conf into "+outFile+"..."
		output = open(outFile, 'w')
		for section in self.list_Sections:
			output.write("["+section+"]\n")
			for opt in sorted(self.Sections[section]): 
				output.write(opt+" : "+self.Sections[section][opt]+"\n") 
			output.write("\n")
		print ">> [INFO] Done"
		return 

