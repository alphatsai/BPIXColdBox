#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from configure import *

class elComandante_conf(configure):

	def __init__(self, debug=False):
		configure.__init__(self, debug)
		self.className = "elComandante_conf"
		self.defaultOutput = "elComandante.conf"

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

