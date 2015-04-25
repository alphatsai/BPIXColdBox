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
		self.hasDefault = False
		self.debug = debug	

		# Pars list
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
		self.list_Directories=["baseDir", "testDefinitions", "moduleDB", "subserverDir", "dataDir", "jumoDir", "keithleyDir", "defaultParameters", "scriptDir"]
		self.list_TestboardAddress=["TB0", "TB1", "TB2", "TB3"]
		self.list_defaultParameters=["Roc", "Full"]
		self.list_subsystem=["Ziel", "Port", "coolingBoxSubscription", "keithleySubscription", "psiSubscription", "xraySubscription", "analysisSubscription"]
		self.list_jumoClient=["port", "programName"]
		self.list_keithleyClient=["port"]
		self.list_lowVoltageClient=["lowVoltageType"]
		self.list_xrayClient=["xrayDevice", "xrayType", "xrfDevice", "xrfType", "xrfTargets", "turnOffHV", "beamOffBetweenTests"]
		self.list_psiClient=["psiVersion"]
		self.list_Transfer=["host", "port", "destination", "user", "checkForTars"]

		# Pars map containor
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
		}

	def loadDefault(self, elComandante_conf_default="elComandante.conf.default"):
		self.defaultConf = elComandante_conf_default
		if not os.path.isfile(self.defaultConf):
			print ">> [ERROR] Can't find "+self.defaultConf+", or it's not a file..."
			sys.exit()
		else: 
			print '>> [INFO] Reading %s...' %self.defaultConf
			self.parser.read(self.defaultConf)
			self.hasDefault = True 
		return

	def fill(self, section="", options=[], output={} ):
		if not self.parser.has_section(section):
			print ">> [ERRO] No section: "+section
		if self.hasDefault:
			for opt in options:
				if self.parser.has_option(section, opt):
					output[opt]=self.parser.get(section, opt)
					if self.debug: 
						print ">> [DEBUG] Got option: {0:>25s} in {1:<20s}".format( opt, section)
				else:
					print ">> [ERROR] No option: "+opt+" in "+section
		else:
			print ">> [ERROR] Please do elComandante_conf.loadDault(file) first." 
			sys.exit()
		return

	def getDefault(self, elComandante_conf_default):
		self.loadDefault(elComandante_conf_default)
		self.fill("Directories",       self.list_Directories,       self.Directories )
		self.fill("TestboardAddress",  self.list_TestboardAddress,  self.TestboardAddress )
		self.fill("defaultParameters", self.list_defaultParameters, self.defaultParameters )
		self.fill("subsystem",         self.list_subsystem,         self.subsystem )
		self.fill("jumoClient",        self.list_jumoClient,        self.jumoClient )
		self.fill("keithleyClient",    self.list_keithleyClient,    self.keithleyClient )
		self.fill("lowVoltageClient",  self.list_lowVoltageClient,  self.lowVoltageClient )
		self.fill("xrayClient",        self.list_xrayClient,        self.xrayClient )
		self.fill("psiClient",         self.list_psiClient,         self.psiClient )
		self.fill("Transfer",          self.list_Transfer,          self.Transfer )
		return

	def listSections(self):
		print ">> [INFO] Call elComandante_conf::listSections()"	
		print ">>        Sections: "
		for sec in self.list_Sections:
			print ">>                  "+sec
		return
	
	def makeNewSection(self, newSec, newOpts={} ):
		if self.debug:  
			print ">> [DEBUG] Call elComandante_conf::makeNewSection( newSec, newOpts  )"	
			print ">>         newSec: "+newSec	
			print ">>         newOpts: "+str(newOpts)
		if newSec in self.Sections:
			print ">> [ERROR] Section "+newSec+" existed"
			return
		self.list_Sections.append(newSec)
		self.Sections[newSec]=newOpts
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
#elini.getDefault("../elComandante.conf")
#elini.listSections()
#elini.listOptions("mySection")
#newopts = {"Opt1":""}
#elini.makeNewSection("mySection1", newopts)
#elini.makeNewSection("mySection1")
#elini.makeNewSection("mySection2")
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
