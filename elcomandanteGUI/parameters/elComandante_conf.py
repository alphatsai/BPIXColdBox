#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

#sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))+'/../')
from ConfigParser import *
from configure import *

class elComandante_conf(configure):

	def __init__(self, debug=False):
		self.className = "elComandante_conf"
		self.defaultOutput = "elComandante.conf"
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

		# Pars map - containor
		self.Sections = { 
			# Default sections and options
			self.list_Sections[0]:{},
			self.list_Sections[1]:{},
			self.list_Sections[2]:{},
			self.list_Sections[3]:{},
			self.list_Sections[4]:{},
			self.list_Sections[5]:{},
			self.list_Sections[6]:{},
			self.list_Sections[7]:{},
			self.list_Sections[8]:{},
			self.list_Sections[9]:{}
			# Can be customily extended by fuction
		}


################ example ################
#elconf = elComandante_conf(debug=True)
##elconf = elComandante_conf()
#elconf.getDefault("../elComandante.conf", True)
#elconf.listSections()
#elconf.listOptions("mySection")
#elconf.makeNewSection("mySection1")
#elconf.makeNewSection("mySection1")
#elconf.makeNewSection("mySection2")
#elconf.makeNewSection("mySection3")
#elconf.listSections()
#elconf.listOptions("mySection")
#elconf.listOptions("mySection1")
#elconf.listOptions("mySection2")
#elconf.makeNewOption("mySection1", "Opt1", "Here")
#elconf.makeNewOption("mySection1", "Opt2", "Here")
#elconf.makeNewOption("mySection2", "Opt1", "Here")
#elconf.listOptions("Transfer")
#elconf.callOption("Transfer", "user" )
#elconf.changeOptValue("mySection1", "Opt3", "There" )
#elconf.changeOptValue("mySection1", "Opt1", "There" )
#elconf.changeOptValue("Transfer", "user", "jtsai" )
#elconf.callOption("Transfer", "user" )
#elconf.callConfig()
#elconf.makeConfig()
