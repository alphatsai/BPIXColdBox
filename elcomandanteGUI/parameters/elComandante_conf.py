#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

#sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from beautyLine import *
from ConfigParser import *

class elComandante_conf:

	def __init__(self, debug=False):
		self.defaultConf = ""
		self.parser = SafeConfigParser()
		self.parser.optionxform = str
		self.hasDefault = False
		self.debug = debug	

		# Pars list -  can be customily extended by fuctions 
		self.list_Sections = [
			"Directories", 
			"TestboardAddress", 
			"defaultParameters", 
			"subsystem", 
			"jumoClient", 
			"keithleyClient", 
			"lowVoltageClient", 
			"xrayClient", 
			"psiClient", 
			"Transfer"
		]
		# Default sections and options in elComandante_conf
		self.list_Default = {
			self.list_Sections[0]:["baseDir", "testDefinitions", "moduleDB", "subserverDir", "dataDir", "jumoDir", "keithleyDir", "defaultParameters", "scriptDir"],
			self.list_Sections[1]:["TB0", "TB1", "TB2", "TB3"],
			self.list_Sections[2]:["Roc", "Full"],
			self.list_Sections[3]:["Ziel", "Port", "coolingBoxSubscription", "keithleySubscription", "psiSubscription", "xraySubscription", "analysisSubscription"],
			self.list_Sections[4]:["port", "programName"],
			self.list_Sections[5]:["port"],
			self.list_Sections[6]:["lowVoltageType"],
			self.list_Sections[7]:["xrayDevice", "xrayType", "xrfDevice", "xrfType", "xrfTargets", "turnOffHV", "beamOffBetweenTests"],
			self.list_Sections[8]:["psiVersion"],
			self.list_Sections[9]:["host", "port", "destination", "user", "checkForTars"]
		}
		# Pars map - default containor
		self.Directories = {}
		self.TestboardAddress = {}
		self.defaultParameters = {}
		self.subsystem = {}
		self.jumoClient = {}
		self.keithleyClient = {}
		self.lowVoltageClient = {}
		self.xrayClient = {}
		self.psiClient = {}
		self.Transfer = {}
		self.Sections = { 
			# Default sections and options
			self.list_Sections[0]:self.Directories,
			self.list_Sections[1]:self.TestboardAddress,
			self.list_Sections[2]:self.defaultParameters,
			self.list_Sections[3]:self.subsystem,
			self.list_Sections[4]:self.jumoClient,
			self.list_Sections[5]:self.keithleyClient,
			self.list_Sections[6]:self.lowVoltageClient,
			self.list_Sections[7]:self.xrayClient,
			self.list_Sections[8]:self.psiClient,
			self.list_Sections[9]:self.Transfer
			# Can be customily extended by fuction
		}

	def loadDefault(self, elComandante_conf_default="elComandante.conf.default" ):
		self.defaultConf = elComandante_conf_default
		if not os.path.isfile(self.defaultConf):
			print ">> [ERROR] Can't find "+self.defaultConf+", or it's not a file..."
		else: 
			self.parser.read(self.defaultConf)
			self.hasDefault = True 
			print '>> [INFO] Loaded %s...' %self.defaultConf
		return

	# It will load default sections and options from elComandante.conf default structure,
	# If you want use new section and options in elComandante.conf, then "addNewSection" has to be "True"
	def getDefault(self, elComandante_conf_default, addNewSection=False ):
		self.loadDefault(elComandante_conf_default)
		print '>> [INFO] Checking default parameter...' 
		for defaultSection in self.list_Default:
			if not self.parser.has_section(defaultSection):
				print ">> [ERROR] No default section: '"+defaultSection+"' in "+elComandante_conf_default
				print ">>         Teminated elComandante_conf::getDefault()"
				return
			else:
				for defaultOpt in self.list_Default[defaultSection]:
					if not self.parser.has_option( defaultSection, defaultOpt): 
						print ">> [ERROR] No default option: '"+defaultOpt+"' under "+defaultSection+" in "+elComandante_conf_default
						print ">>         Teminated elComandante_conf::getDefault()"
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
		return


	def listSections(self):
		print ">> [INFO] Call elComandante_conf::listSections()"	
		print ">>        Sections: "
		for sec in self.list_Sections:
			print ">>                  "+sec
		return
	
	#def makeNewSection(self, newSec, newOpts={} ):
	def makeNewSection(self, newSec ):
		if self.debug:  
			print ">> [DEBUG] Call elComandante_conf::makeNewSection( newSec, newOpts  )"	
			print ">>         newSec: "+newSec	
			#print ">>         newOpts: "+str(newOpts)
		if newSec in self.Sections:
			print ">> [ERROR] Section "+newSec+" existed"
			return
		else:
			self.list_Sections.append(newSec)
			self.Sections[newSec]={}
		return

	def makeNewOption(self, secName, newOptsName, newValue="" ):
		if self.debug:  
			print ">> [DEBUG] Call elComandante_conf::makeNewOption( secName, newOptsName, newValue  )"	
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
		
	def changeOptValue(self, secName, optName, newValue ):
		if self.debug:  
			print ">> [DEBUG] Call elComandante_conf::changeOptValue( secName, optName, newValue  )"	
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

	def listOptions(self, secName ):
		if secName in self.Sections:
			print ">> [INFO] Call elComandante_conf::listOptions( "+secName+" )" 
			print ">>        Options: "
			for opt in self.Sections[secName]:
				print ">>                "+opt
		else:
			print ">> [INFO] Call elComandante_conf::listOptions( "+secName+" )" 
			print ">> [ERROR] Not found section "+secName
		return

	def callOption(self, secName, optName ):
		if secName in self.Sections:
			if optName in self.Sections[secName]:
				print ">> [INFO] Call elComandante_conf::callOption( "+secName+", "+optName+" )" 
				print ">>        Value: "+self.Sections[secName][optName]
			else:
				print ">> [INFO] Call elComandante_conf::callOption( "+secName+", "+optName+" )" 
				print ">> [ERROR] Not found option "+optName+" in "+secName
		else:
			print ">> [INFO] Call elComandante_conf::callOption( "+secName+", "+optName+" )" 
			print ">> [ERROR] Not found section "+secName
		return

	def callConfig(self):
		print "\n############ Current elComandante.conf #################\n"
		for section in self.list_Sections:
			print " ["+section+"]"
			for opt in sorted(self.Sections[section]): 
				print " "+opt+" : "+self.Sections[section][opt] 
			print "\n"
		return

	def makeConfig(self, outFile="./elComandante.conf" ):
		print ">> [INFO] Writing conf into "+outFile+"..."
		output = open(outFile, 'w')
		for section in self.list_Sections:
			output.write("["+section+"]\n")
			for opt in sorted(self.Sections[section]): 
				output.write(opt+" : "+self.Sections[section][opt]+"\n") 
			output.write("\n")
		return ">> [INFO] Done"
		

################ example ################
#elini = elComandante_conf(debug=True)
##elini = elComandante_conf()
#elini.getDefault("../elComandante.conf", True)
#elini.listSections()
#elini.listOptions("mySection")
#elini.makeNewSection("mySection1")
#elini.makeNewSection("mySection1")
#elini.makeNewSection("mySection2")
#elini.makeNewSection("mySection3")
#elini.listSections()
#elini.listOptions("mySection")
#elini.listOptions("mySection1")
#elini.listOptions("mySection2")
#elini.makeNewOption("mySection1", "Opt1", "Here")
#elini.makeNewOption("mySection1", "Opt2", "Here")
#elini.makeNewOption("mySection2", "Opt1", "Here")
#elini.listOptions("Transfer")
#elini.callOption("Transfer", "user" )
#elini.changeOptValue("mySection1", "Opt3", "There" )
#elini.changeOptValue("mySection1", "Opt1", "There" )
#elini.changeOptValue("Transfer", "user", "jtsai" )
#elini.callOption("Transfer", "user" )
#elini.callConfig()
#elini.makeConfig()
