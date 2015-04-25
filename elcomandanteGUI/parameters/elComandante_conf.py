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
		self.list_Sections=["Directories", "TestboardAddress", "defaultParameters", "subsystem", "jumoClient", "keithleyClient", "lowVoltageClient", "xrayClient", "psiClient", "Transfer"]
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
			"Directories":self.Directories,
			"TestboardAddress":self.TestboardAddress,
			"defaultParameters":self.defaultParameters,
			"subsystem":self.subsystem,
			"jumoClient":self.jumoClient,
			"keithleyClient":self.keithleyClient,
			"lowVoltageClient":self.lowVoltageClient,
			"xrayClient":self.xrayClient,
			"psiClient":self.psiClient,
			"Transfer":self.Transfer
		}
	
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

	def loadDefault(self, elComandante_conf_default):
		self.defaultConf = elComandante_conf_default
		if not os.path.isfile(self.defaultConf):
			print ">> [ERROR] Can't find "+self.defaultConf+", or it's not a file..."
			sys.exit()
		else: 
			print '>> [INFO] Reading %s...' %self.defaultConf
			self.parser.read(self.defaultConf)
			self.hasDefault = True 

	def fill(self, section, options, output ):
		if self.hasDefault:
			for opt in options:
				if self.parser.has_option(section, opt):
					output[opt]=self.parser.get(section, opt)
					if self.debug: 
						print ">> [DEBUG] Got option: {0:>25s} in {1:<20s}".format( opt, section)
				else:
					print ">> [WARNING] No option: "+opt+" in "+section
		else:
			print ">> [ERROR] Please do elComandante_conf.loadDault(file) first." 
			sys.exit()

	def printConfig(self):
		print "\n############ Current elComandante.conf #################\n"
		for section in self.list_Sections:
			print " ["+section+"]"
			for opt in sorted(self.Sections[section]): 
				print " "+opt+" : "+self.Sections[section][opt] 
			print "\n"

	def makeConfig(self, outFile="./elComandante.conf" ):
		print ">> [INFO] Writing conf into "+outFile+"..."
		output = open(outFile, 'w')
		for section in self.list_Sections:
			output.write("["+section+"]\n")
			for opt in sorted(self.Sections[section]): 
				output.write(opt+" : "+self.Sections[section][opt]+"\n") 
			output.write("\n")
		print ">> [INFO] Done"
		

################ test ################
#elini = elComandante_conf(debug=True)
#elini.getDefault("../elComandante.conf")
#elini.printConfig()
#elini.makeConfig()
