#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <stdio.h>
#include "TGraph.h"
#include "TH1F.h"
#include "TF1.h"
#include "TLegend.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TLine.h"
#include <string>

const double unitA=-1000000; //uA
const double unitV=-1;       //Vol

void IVCurves(char* fname)
{
    TGraph *gr_vi = new TGraph(fname);
    TCanvas *c1 = new TCanvas("c1","",720,640);

    for(int i=0;i<gr_vi->GetN();i++){
        double x, y;
        gr_vi->GetPoint(i,x,y);
        gr_vi->SetPoint(i,x*unitV,y*unitA);
    }
    string s=string(fname);

    std::cout << s << std::endl;
    
    size_t pos=s.find("_IV_");
    size_t pos1=s.find("2015");
    
    string outname = "IVCurves/" + s.substr(0,5) + "_" + s.substr(pos-3,10) + s.substr(pos1-1,18)  + ".png";
    
    //cout << outname << endl;

    c1->SetFillColor(0);
    c1->SetLogy(1);
    gr_vi->SetMinimum(0.001);
    gr_vi->SetMarkerColor(4);
    gr_vi->SetMarkerStyle(21);
    gr_vi->SetMarkerSize(1.);
    gr_vi->SetLineWidth(3);
    gr_vi->SetTitle("");
    gr_vi->GetXaxis()->SetTitle("High voltage [V]");
    gr_vi->GetYaxis()->SetTitle("Leakage current [#muA]");
    gr_vi->Draw("ALPTEXT");
    c1->SaveAs(outname.c_str());

}


