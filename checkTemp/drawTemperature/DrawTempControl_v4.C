/*
   Purpose : draw temperature, relative humidity, and dew point as a function of time 
   Author  : Dr. Yeng-Ming (Jacky) Tzeng 
   eMail   : ymtzeng@cern.ch
   version : 1
Data    :


   */

#include "TGraph.h"
#include "TH1F.h"
#include "TLegend.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TLine.h"
#include <iostream>

const float a_ = 6.1121;
const float b_ = 17.368;// 18.678;
const float c_ = 238.88;// 257.14;
const float d_ = 234.5;
float rm(float T, float RH);

float MarkerSize_ = 1.0;    // 0.7

void DrawTempControl_v4(){

    double maxX = -1;
    double minX = -1;
    TCanvas *c1 = new TCanvas("c1","",720,640);
    c1->cd();
    TPad *pad = new TPad("pad","",0,0,0.93,1);
    pad->Draw();
    pad->cd();


    TGraph *temp = new TGraph("log_temperature_current");
    TGraph *humi = new TGraph("log_humidity_current");
    //TGraph *dewpoint = new TGraph("LOG/log_humidity_current");
    TGraph *dewpoint = new TGraph("log_dewPoint_current");
    double x_first = 0;
    double xt_first = 0;
    double xd_first = 0;

    if(true){
        double xt_=0;
        double yt_=0;
        temp->GetPoint(0,xt_,yt_);
        xt_first = xt_;
        humi->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
        dewpoint->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
    }


    for(int i=0;i<temp->GetN();i++){
        double x_,xt_,xd_;
        double y_,yt_,yd_;
        temp->GetPoint(i,xt_,yt_);
        //if(i==0) xt_first = xt_;
        temp->SetPoint(i,(xt_-xt_first)/60.,yt_);
        if(i==0) minX = (xt_-xt_first)/60.;
        if(i==temp->GetN()-1) maxX = (xt_-xt_first)/60.;
    }
    for(int i=0;i<humi->GetN();i++){
        double x_;
        double y_;
        humi->GetPoint(i,x_,y_);
        //if(i==0) x_first = x_;
        if(i==0) x_first = xt_first;
        humi->SetPoint(i,(x_-x_first)/60.,y_);
        if(maxX< (x_-x_first)/60.) maxX = (x_-x_first)/60.;
    }
    for(int i=0;i<dewpoint->GetN();i++){
        double xd_;
        double yd_;
        dewpoint->GetPoint(i,xd_,yd_);
        //if(i==0) xd_first = xd_;
        if(i==0) xd_first = xt_first;
        dewpoint->SetPoint(i,(xd_-xd_first)/60.,yd_);
        if(maxX< (xd_-xd_first)/60.) maxX = (xd_-xd_first)/60.;
    }
    //maxX = 120;

    c1->SetGridx(1);
    c1->SetGridy(1);
    temp->SetMarkerStyle(22);
    temp->SetMarkerSize(MarkerSize_);
    temp->SetMarkerColor(kBlue-2);
    temp->SetTitle("4 loads of 3W each + Air Flow (2.5 L/min)");
    temp->SetTitle("");
    temp->GetXaxis()->SetTitle("Time [min]");
    temp->GetYaxis()->SetTitle("Temperature [^{o}C]");
    temp->GetYaxis()->SetRangeUser(-50,20);
    temp->GetXaxis()->SetRangeUser(0,maxX);
    temp->Draw("AP");

    dewpoint->SetMarkerStyle(22);
    dewpoint->SetMarkerSize(MarkerSize_);
    dewpoint->SetMarkerColor(kGreen-2);
    dewpoint->GetXaxis()->SetRangeUser(0,maxX);
    dewpoint->Draw("same, eP");

    //TLine *line = new TLine(minX,-20, maxX,-20);
    //line->SetLineColor(kYellow-2);
    //line->SetLineStyle(2);
    //line->SetLineWidth(4);
    //line->Draw();

    c1->cd();
    TPad *overlay = new TPad("overlay","",0,0,0.93,1);
    overlay->SetFillStyle(4000);
    overlay->SetFillColor(0);
    overlay->SetFrameFillStyle(4000);
    overlay->Draw();
    overlay->cd();

    overlay->SetGridx(1);
    overlay->SetGridy(1);
   
   	humi->Draw("ap,Y+");
    humi->GetYaxis()->SetLabelSize(0.04);
    humi->GetYaxis()->SetTicks("+");
    humi->SetTitle("");
    humi->GetYaxis()->SetTitle("Relative humidity [%]");
    humi->GetYaxis()->SetRangeUser(0,35);
    humi->SetMarkerStyle(22);
    humi->SetMarkerSize(MarkerSize_);
    humi->SetMarkerColor(kRed-2);
    humi->GetXaxis()->SetRangeUser(0,maxX);


    TLegend *legend_nm = new TLegend(0.52,0.74,0.7,0.9);
    legend_nm->SetBorderSize(0);
    legend_nm->SetFillColor(0);
    legend_nm->SetFillStyle(0);
    legend_nm->SetNColumns(1);
    legend_nm->SetTextSize(0.035);
    legend_nm->SetTextSizePixels(25);

    legend_nm->AddEntry(temp,"Temperature (JUMO)", "p" );
    legend_nm->AddEntry(dewpoint,"Dew point", "p" );
    legend_nm->AddEntry(humi,"Relative humidity", "p" );
    legend_nm->Draw();

    c1->SaveAs("performance_FOLDER.png");
}

// http://en.wikipedia.org/wiki/Dew_point
float rm(float T, float RH){
    return log( (RH/100.) * exp((b_-T/d_)*(T/(c_+T)))  );  
}

