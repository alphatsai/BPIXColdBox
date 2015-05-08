#!/usr/bin/env python
import sys, math

if len(sys.argv) < 3:
	print '>> [INFO] Please input maximum temperature and angle'
	print '>>        Ex. ./cosine [max T] [angle]'
	sys.exit()

maxTemp = sys.argv[1]
angle = sys.argv[2]
graidian = 5

temperature = float(maxTemp)*math.cos(int(angle)*graidian*math.pi/180)
print '%.2f'%temperature
