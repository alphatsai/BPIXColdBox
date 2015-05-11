#!/usr/bin/python
import os, re, sys, shutil
import math, time
from ROOT import *

c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 6 )
c1.GetFrame().SetBorderMode( -1 )

sh = TSignalHandler( kSigInterrupt, False )
sh.Add()
sh.Connect( "Notified()", "TROOT", gROOT, "SetInterrupt()" )

inputf = '../example/logfiles/temperature.log'
timeUnit=60
print '>> [INFO] Reading %s...'%inputf
while (1):
	gh = TGraph(inputf)

	x0, y0= Double(0), Double(0)
	gh.GetPoint(0, x0, y0)
	for i in xrange(0, gh.GetN()):
		x, y= Double(0), Double(0)
		gh.GetPoint(i,x,y)
		gh.SetPoint(i,(x-x0)/timeUnit, y)

	gh.SetMarkerStyle(22)
	gh.SetMarkerSize(1)
	gh.SetMarkerColor(kBlue-2)
	gh.SetLineWidth(2)
	gh.SetLineColor(kRed)
	gh.SetTitle("")
	gh.GetXaxis().SetTitle("Time [min]")
	gh.GetYaxis().SetTitle("Temperature [#circC]")
	gh.Draw("APL")

	c1.Modified()
	c1.Update()
	time.sleep(4)
	if gROOT.IsInterrupted():      # allow user interrupt
		c1.SaveAs('temperature.pdf')
		break
	

