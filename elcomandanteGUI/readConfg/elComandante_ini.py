#!/usr/bin/env python
import os, re, sys, shutil
import math, ROOT

from configure import *

class elComandante_ini(configure):

	def __init__(self, debug=False):
		configure.__init__(self, debug)
		self.className = "elComandante_ini"
		self.defaultOutput = "elComandante.ini"

		# Pars list -  can be customily extended by fuctions 
		self.list_Sections = [
			"Modules",
			"ModuleType",
			"TestboardUse",
			"Cycle",
			"IV",
			"LeakageCurrent",
			"Keithley",
			"LowVoltage",
			"CoolingBox",
			"Xray",
			"Environment Xrf",
			"Environment Mo", 
			"Environment Ag",
			"Environment Ba",
			"Test Trim",
			"Analysis VcalCalibrationStepAnalysisMo",
			"Analysis VcalCalibrationStepAnalysisAg",
			"Analysis VcalCalibrationStepAnalysisBa",
			"Analysis VcalVsThresholdAnalysis",
			"Analysis VcalCalibrationAnalysis",
			"Tests",
			"OperationDetails",
		]
		# Default sections and options in elComandante_conf
		self.list_Default = {
			self.list_Sections[0]:["TB0", "TB1", "TB2", "TB3"],
			self.list_Sections[1]:["TB0", "TB1", "TB2", "TB3"],
			self.list_Sections[2]:["TB0", "TB1", "TB2", "TB3"],
			self.list_Sections[3]:["highTemp", "lowTemp", "nCycles"],
			self.list_Sections[4]:["Start", "Stop", "Step", "Delay"],
			self.list_Sections[5]:["Duration"],
			self.list_Sections[6]:["KeithleyUse", "BiasVoltage"],
			self.list_Sections[7]:["LowVoltageUse"],
			self.list_Sections[8]:["CoolingBoxUse"],
			self.list_Sections[9]:["XrayUse"],
			self.list_Sections[10]:["Temperature", "XrayVoltage", "XrayCurrent", "XrayTarget"],
			self.list_Sections[11]:["Temperature", "XrayVoltage", "XrayCurrent", "XrayTarget"],
			self.list_Sections[12]:["Temperature", "XrayVoltage", "XrayCurrent", "XrayTarget"],
			self.list_Sections[13]:["Temperature", "XrayVoltage", "XrayCurrent", "XrayTarget"],
			self.list_Sections[14]:["testParameters"],
			self.list_Sections[15]:["command"],
			self.list_Sections[16]:["command"],
			self.list_Sections[17]:["command"],
			self.list_Sections[18]:["command"],
			self.list_Sections[19]:["command"],
			self.list_Sections[20]:["TestDescription", "Test"],
			self.list_Sections[21]:["Hostname", "TestCenter", "Operator"],
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
			self.list_Sections[9]:{},
			self.list_Sections[10]:{},
			self.list_Sections[11]:{},
			self.list_Sections[12]:{},
			self.list_Sections[13]:{},
			self.list_Sections[14]:{},
			self.list_Sections[15]:{},
			self.list_Sections[16]:{},
			self.list_Sections[17]:{},
			self.list_Sections[18]:{},
			self.list_Sections[19]:{},
			self.list_Sections[20]:{},
			self.list_Sections[21]:{},
			# Can be customily extended by fuction
		}

