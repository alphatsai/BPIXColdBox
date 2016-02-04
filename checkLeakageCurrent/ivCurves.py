#!/usr/bin/python
import os, re, sys, shutil, commands
import math, time
from ROOT import *
from optparse import OptionParser

# usage description
usage = """
Usage: """+sys.argv[0]+""" [options]
Example: """+sys.argv[0]+""" -i M3187_FullQualification_2016-02-02_10h14m_1454404441
For more help: """+sys.argv[0]+""" --help
"""

# Option parameters
parser = OptionParser(usage=usage)
parser.add_option("-i", "--inputDir", dest="inputDir",
                  help="Input file")
parser.add_option("-o", "--outputr", dest="output", default=".",
                  help="Output path")
parser.add_option("-s", "--sleep", dest="sleep", default=5,
                  help="Sleep time")
parser.add_option("-X", "--xMax", dest="xMax", default=310,
                  help="x-axis max")
parser.add_option("-x", "--xMin", dest="xMin", default=0,
                  help="x-axis min")
parser.add_option("-b", "--xBin", dest="xBin", default=30,
                  help="x-axis bin")
(options, args) = parser.parse_args()

if not options.inputDir:
    print usage
    sys.exit()
if not os.path.isdir(options.inputDir):
    print ">> [ERROR] Can't find "+options.inputDir+", or it's not a directory..."
    sys.exit()

mName = options.inputDir.split("_")[0]
mTime = options.inputDir.split("_")[2]
listDir = commands.getoutput('ls '+options.inputDir).split("\n")
ivDirs  = filter( lambda x: x.find('IV') > -1 , listDir )
ivlog = 'ivCurve.log'

unitA=-1000000.  #uA
unitV=-1.        #Vol
yMax=0
yMin=0.1

print '>> [INFO] Get %d IV dir in %s'%( len(ivDirs), options.inputDir )
print '>>        -->  %s'%( ivDirs )
print '>> [INFO] Turn off in %d sec.'%( options.sleep )

ghMap = {}
for ivDir in ivDirs:
    ivlogPath = options.inputDir+"/"+ivDir+"/"+ivlog
    if not os.path.isfile(ivlogPath):
        print '>> [WARNNING] No %s in %s'%( ivlog, ivDir )
        continue
    gh = TGraph(options.inputDir+"/"+ivDir+"/"+ivlog)

    x0, y0= Double(0), Double(0)
    gh.GetPoint(0, x0, y0)
    for i in xrange(0, gh.GetN()):
	x, y= Double(0), Double(0)
	gh.GetPoint(i,x,y)
        if y > 0 :
            y=-1e-10
	gh.SetPoint(i,x*unitV,y*unitA)
        if yMax < y*unitA:
            yMax = y*unitA
        if yMin > y*unitA:
            yMin = y*unitA

    ghMap[ivDir]=gh

c1 = TCanvas("c1", "",1560,33,928,763);
c1.SetHighLightColor(2);
c1.Range(-89.1892,-2.628028,327.027,1.176471);
c1.SetFillColor(0);
c1.SetBorderMode(0);
c1.SetBorderSize(2);
c1.SetLogy();
c1.SetLeftMargin(0.2142857);
c1.SetRightMargin(0.06493507);
c1.SetTopMargin(0.04638472);
c1.SetBottomMargin(0.165075);
c1.SetFrameBorderMode(0);
c1.SetFrameBorderMode(0);
gStyle.SetOptStat(0);

h = TH1D("base", "", options.xBin, options.xMin, options.xMax )
h.SetMaximum(yMax*100.)
h.SetMinimum(yMin)
h.GetXaxis().SetTitle("Voltage [V]");
h.GetXaxis().SetLabelFont(42);
h.GetXaxis().SetLabelSize(0.06);
h.GetXaxis().SetTitleSize(0.07);
h.GetXaxis().SetTitleFont(42);
h.GetYaxis().SetTitle("Leakage current [#muA]");
h.GetYaxis().SetLabelFont(42);
h.GetYaxis().SetLabelSize(0.06);
h.GetYaxis().SetTitleSize(0.08);
h.GetYaxis().SetTitleOffset(1.1);
h.GetYaxis().SetTitleFont(42);
h.Draw()

leg = TLegend(0.2521645,0.7387755,0.5205628,0.9346939)
leg.SetHeader(mName+", "+mTime)
leg.SetBorderSize(0)
leg.SetLineStyle(0)
leg.SetLineWidth(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)

iColor=1
for ivDir in sorted(ghMap):
    ghMap[ivDir].SetMarkerStyle(8)
    ghMap[ivDir].SetMarkerSize(2)
    ghMap[ivDir].SetMarkerColor(iColor)
    ghMap[ivDir].SetLineColor(iColor)
    ghMap[ivDir].SetLineWidth(2)
    ghMap[ivDir].Draw("LPSAME")
    leg.AddEntry( ghMap[ivDir], ivDir, "lp")
    iColor+=1

leg.Draw()
c1.SaveAs(options.output+"/ivCurves_"+options.inputDir+".pdf")
time.sleep(float(options.sleep))
