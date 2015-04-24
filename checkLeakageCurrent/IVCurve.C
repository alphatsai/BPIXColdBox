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
//#include "CMSstyle.C"
#include "setTDRStyle.C"
#define MAXPOINTS 1000;

void IVCurve()
{

	setTDRStyle();
	//CMSstyle();
	TGraph *gr_vi = new TGraph("09July_SigleChip207/RecordVI");
	gr_vi->UseCurrentStyle();

	/////////////////////////////////////////////////////////


    TCanvas *c1 = new TCanvas("c1","",720,640);
	c1->SetFillColor(0);
	//c1->SetGrid();


	//cout<<"Init parameters: ("<<P0_init<<","<<P1_init<<","<<P2_init<<")"<<endl;
	TF1 *func = new TF1("func","pol1",50.,200);
	gStyle->SetOptFit(101);//Para quete salgan los parametros en el canvas
	func->SetParameters(0,1);
	func->SetParName(1,"slope");
	func->SetParName(0,"intercept");
	func->SetLineColor(2);


	//cout << ModType2<<endl;
	gr_vi->SetMarkerColor(4);
	gr_vi->SetMarkerStyle(21);
	gr_vi->SetMarkerSize(1.);
	gr_vi->SetLineWidth(3);
	gr_vi->SetTitle("");
	gr_vi->GetXaxis()->SetTitle("High voltage [V]");
	gr_vi->GetYaxis()->SetTitle("Leakage current [#muA]");
	gr_vi->GetXaxis()->SetTitleSize(0.05);
	gr_vi->GetYaxis()->SetTitleSize(0.05);
	gr_vi->GetXaxis()->SetLabelSize(0.05);
	gr_vi->GetYaxis()->SetLabelSize(0.05);
	gr_vi->Fit(func,"","",70,240);
	gr_vi->Draw("ALP");

	c1->SaveAs("png/09July_SigleChip207_IVCurve_2.png");

}


