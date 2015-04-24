#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

#sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from beautyLine import *
from ConfigParser import *

class elComandante_ini:
	def __init__(self):
		self.defaultConf = ""
		self.parser = SafeConfigParser()
		# Pars list
		self.list_Sections=["Directories", "TestboardAddress", "defaultParameters", "jumoClient", "keithleyClient", "lowVoltageClient", "xrayClient", "psiClient", "Transfer"]
		self.list_Directories=["baseDir", "testDefinitions", "moduleDB", "subserverDir", "dataDir", "jumoDir", "keithleyDir", "defaultParameters", "scriptDir"]
		self.list_TestboardAddress=["TB0", "TB1", "TB2", "TB3"]
		self.list_defaultParameters=["Roc", "Full"]
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
		self.Transfer = {}
	
	def getDefault(self, elComandante_ini_default):
		self.defaultConf = elComandante_ini_default
		if not os.path.isfile(self.defaultConf):
			print ">> [ERROR] Can't find "+self.defaultConf+", or it's not a file..."
			sys.exit()
		else: 
			print '>> Reading %s...' %self.defaultConf
			self.parser.read(self.defaultFile)

			self.fill("Directories",       self.list_Directories,       self.Directories )
			self.fill("TestboardAddress",  self.list_TestboardAddress,  self.TestboardAddress )
			self.fill("defaultParameters", self.list_defaultParameters, self.TestboardAddress )
			self.fill("subsystem",         self.list_subsystem,         self.subsystem )
			self.fill("jumoClient",        self.list_jumoClient,        self.jumoClient )
			self.fill("keithleyClient",    self.list_keithleyClient,    self.keithleyClient )
			self.fill("lowVoltageClient",  self.list_lowVoltageClient,  self.lowVoltageClient )
			self.fill("xrayClient",        self.list_xrayClient,        self.xrayClient )
			self.fill("psiClient",         self.list_psiClient,         self.psiClient )
			self.fill("Transfer",          self.list_Transfer,          self.Transfer )

	def fill(self, section, options, output ):
		#if self.parser
		for opt in options
			if self.parser.has_option(section, opt):
				output[opt]=parser.get(section, opt)
			else:
				print ">> [Warning] No option: "+opt+" in "+section

	def printConfig(self):






#			# Fill [Directories]
#			for opt in self.list_Directories
#				if parser.has_option("Directories", opt):
#					self.Directories[opt]=parser.get("Directories", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in Directories"
#
#			# Fill [TestboardAddress]
#			for opt in self.list_TestboardAddress
#				if parser.has_option("TestboardAddress", opt):
#					self.TestboardAddress[opt]=parser.get("TestboardAddress", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in TestboardAddress"
#					 
#			# Fill [defaultParameters]
#			for opt in self.list_defaultParameters
#				if parser.has_option("defaultParameters", opt):
#					self.defaultParameters[opt]=parser.get("defaultParameters", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in defaultParameters"
#					 
#			# Fill [subsystem]
#			for opt in self.list_subsystem
#				if parser.has_option("subsystem", opt):
#					self.subsystem[opt]=parser.get("subsystem", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in subsystem"
#					 
#			# Fill [jumoClient]
#			for opt in self.list_jumoClient
#				if parser.has_option("jumoClient", opt):
#					self.jumoClient[opt]=parser.get("jumoClient", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in jumoClient"
#					 
#			# Fill [keithleyClient]
#			for opt in self.list_keithleyClient
#				if parser.has_option("keithleyClient", opt):
#					self.keithleyClient[opt]=parser.get("keithleyClient", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in keithleyClient"
#					 
#			# Fill [lowVoltageClient]
#			for opt in self.list_lowVoltageClient
#				if parser.has_option("lowVoltageClient", opt):
#					self.lowVoltageClient[opt]=parser.get("lowVoltageClient", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in lowVoltageClient"
#					 
#			# Fill [xrayClient]
#			for opt in self.list_xrayClient
#				if parser.has_option("xrayClient", opt):
#					self.xrayClient[opt]=parser.get("xrayClient", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in xrayClient"
#					 
#			# Fill [psiClient]
#			for opt in self.list_psiClient
#				if parser.has_option("psiClient", opt):
#					self.psiClient[opt]=parser.get("psiClient", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in psiClient"
#					 
#			# Fill [Transfer]
#			for opt in self.list_Transfer
#				if parser.has_option("Transfer", opt):
#					self.Transfer[opt]=parser.get("Transfer", opt)
#				else:
#					print ">> [Warning] No option: "+opt+" in Transfer" 
