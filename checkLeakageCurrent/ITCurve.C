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

void ITCurve()
{

	//CMSstyle();
	setTDRStyle();
	//TGraph *gr_ti = new TGraph("09July_SigleChip207/RecordTI");
	TGraph *gr_ti = new TGraph("09July_SigleChip207/RecordTI_PT1000");
	gr_ti->UseCurrentStyle();

	/////////////////////////////////////////////////////////


    TCanvas *c1 = new TCanvas("c1","",720,640);
	c1->SetFillColor(0);
	//c1->SetGrid();


	//cout<<"Init parameters: ("<<P0_init<<","<<P1_init<<","<<P2_init<<")"<<endl;
	//TF1 *func = new TF1("func","pol1",50.,200);
	//TF1 *func = new TF1("func","-0.00816*[0]*(x+273.15)*(x+273.15)*exp([1]*(1/(x+273.15)-1/273.15))/(273.15)/(273.15)",-30.,25);
	//TF1 *func = new TF1("func","-0.01275*[0]*(x+273.15)*(x+273.15)*exp([1]*(1/(x+273.15)-1/273.15))/(273.15)/(273.15)",-30.,25);
	//TF1 *func = new TF1("func","-0.01275*(x+273.15)*(x+273.15)*exp([0]*(1/(x+273.15)-1/273.15))/(273.15)/(273.15)",-30.,25);
	TF1 *func = new TF1("func","-0.00816*(x+273.15)*(x+273.15)*exp([0]*(1/(x+273.15)-1/273.15))/(273.15)/(273.15)",-30.,25);
	func->SetLineWidth(2);
	//func->SetParameter(2,1);
	//func->SetParName(0,-0.00816);
	//func->SetParName(1,1);
	//func->SetParName(2,1);


	//cout << ModType2<<endl;
	gr_ti->SetMarkerColor(4);
	gr_ti->SetMarkerStyle(21);
	gr_ti->SetMarkerSize(1.);
	gr_ti->SetLineWidth(3);
	gr_ti->SetTitle("");
	gr_ti->GetXaxis()->SetTitle("Temperature [#circC]");
	gr_ti->GetYaxis()->SetTitle("Leakage current [#muA]");
	gr_ti->GetXaxis()->SetTitleSize(0.05);
	gr_ti->GetYaxis()->SetTitleSize(0.05);
	gr_ti->GetXaxis()->SetLabelSize(0.05);
	gr_ti->GetYaxis()->SetLabelSize(0.05);
	gr_ti->GetXaxis()->SetRangeUser(-30,25);
	gr_ti->Fit(func,"","",-30,25);
	gr_ti->Draw("AP");

	//c1->SaveAs("png/09July_SigleChip207_ITCurve_3.png");
	c1->SaveAs("png/09July_SigleChip207_ITCurve_PT1000_3.png");

}


