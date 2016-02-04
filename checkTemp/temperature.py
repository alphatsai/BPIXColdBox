#!/usr/bin/python
import os, re, sys, shutil
import math, time
from ROOT import *

c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 6 )
c1.GetFrame().SetBorderMode( -1 )
c1.Divide(1,2)

sh = TSignalHandler( kSigInterrupt, False )
sh.Add()
sh.Connect( "Notified()", "TROOT", gROOT, "SetInterrupt()" )

inputf = 'logfiles/temperature.log'
inputf2 = 'logfiles/humidity.log'
timeUnit=60
print '>> [INFO] Reading %s...'%inputf
while (1):
	
	global count
	gh = TGraph(inputf)
	gh2 = TGraph(inputf2)
	
	x0, y0= Double(0), Double(0)
	gh.GetPoint(0, x0, y0)
	count=0
	up=0
	down=0
	for i in xrange(0, gh.GetN()):
		x, y= Double(0), Double(0)
		gh.GetPoint(i,x,y)
		gh.SetPoint(i,(x-x0)/timeUnit, y)
		inc=y-y0
		if inc<0 and y<-23.5:
			down=1
			y0=y
		if inc>0 and down and y>18.5:
			up=1
			y0=y
		if up and down and inc<0:
			count=count+1
			up=0
			down=0
	gh2.GetPoint(0, x0, y0)
	for i in xrange(0, gh2.GetN()):
		x, y= Double(0), Double(0)
		gh2.GetPoint(i,x,y)
		gh2.SetPoint(i,(x-x0)/timeUnit, y)
	
	ssc="Cycles done "+str(count)
	gh.SetMarkerStyle(22)
	gh.SetMarkerSize(1)
	gh.SetMarkerColor(kBlue-2)
	gh.SetLineWidth(2)
	gh.SetLineColor(kRed)
	gh.SetTitle(ssc)
	gh.GetXaxis().SetTitle("Time [min]")
	gh.GetXaxis().SetLabelFont(42);
	gh.GetXaxis().SetLabelSize(0.04);
	#gh.GetXaxis().SetTitleSize(0.06);
	gh.GetXaxis().SetTitleFont(42);
	gh.GetYaxis().SetTitle("Temperature [#circC]");
	gh.GetYaxis().SetLabelFont(42);
	gh.GetYaxis().SetLabelSize(0.09);
	gh.GetYaxis().SetTitleSize(0.08);
	gh.GetYaxis().SetTitleOffset(0.55);
	
	gh2.SetMarkerStyle(22)
	gh2.SetMarkerSize(1)
	gh2.SetMarkerColor(kBlue-2)
	gh2.SetLineWidth(2)
	gh2.SetLineColor(kRed)
	gh2.SetTitle("")
	gh2.GetXaxis().SetTitle("Time [min]")
	gh2.GetXaxis().SetLabelFont(42);
	gh2.GetXaxis().SetLabelSize(0.04);
	#gh2.GetXaxis().SetTitleSize(0.06);
	gh2.GetXaxis().SetTitleFont(42);
	gh2.GetYaxis().SetTitle("RH [%]")
	gh2.GetYaxis().SetLabelFont(42);
	gh2.GetYaxis().SetLabelSize(0.09);
	gh2.GetYaxis().SetTitleSize(0.08);
	gh2.GetYaxis().SetTitleOffset(0.55);
	
	c1.cd(1)
	gh.Draw("APL")
	c1.cd(2)
	gh2.Draw("APL")
	
	c1.Modified()
	c1.Update()
	time.sleep(4)
	if gROOT.IsInterrupted():      # allow user interrupt
		c1.SaveAs('temperature.pdf')
		break


