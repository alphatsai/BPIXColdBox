/*
   Purpose : draw temperature, relative temp5dity, and dew point as a function of time 
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

float MarkerSize_ = 0.7 ;   // 0.7
//float MarkerSize_ = 1 ;   // 0.7

void pt1000Line4(){

    double maxX = -1;
    double minX = -1;
    TCanvas *c1 = new TCanvas("c1","",720,640);
    c1->cd();


    TGraph *temp = new TGraph("log_temperature_current");
    TGraph *temp3 = new TGraph("Labview_record_3_txt_Cal.txt");
    TGraph *temp4 = new TGraph("Labview_record_4_txt_Cal.txt");
    TGraph *temp2 = new TGraph("Labview_record_2_txt_Cal.txt");
    TGraph *temp5 = new TGraph("Labview_record_5_txt_Cal.txt");
    TGraph *temp1 = new TGraph("Labview_record_1_txt_Cal.txt");
    double first_5 = 0;
    double first_3 = 0;
    double first_4 = 0;
    double xt_first = 0;
    double first_1 = 0;
    double first_2 = 0;

    if(true){
        double xt_=0;
        double yt_=0;
        temp->GetPoint(0,xt_,yt_);
        xt_first = xt_;
        temp3->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
        temp4->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
        temp5->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
        temp1->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
        temp2->GetPoint(0,xt_,yt_);
        if(xt_<xt_first) xt_first = xt_;
    }


    for(int i=0;i<temp->GetN();i++){
        double x_,xt_;
        double y_,yt_;
        temp->GetPoint(i,xt_,yt_);
        temp->SetPoint(i,(xt_-xt_first)/60.,yt_);
        if(i==0) minX = (xt_-xt_first)/60.;
        if(i==temp->GetN()-1) maxX = (xt_-xt_first)/60.;
    }
    for(int i=0;i<temp3->GetN();i++){
        double x_;
        double y_;
        temp3->GetPoint(i,x_,y_);
        if(i==0) first_3 = xt_first; 
        	temp3->SetPoint(i,(x_-first_3)/60.,y_);
        if( maxX < (x_-first_3)/60.) maxX = (x_-first_3)/60.;
    }
    for(int i=0;i<temp4->GetN();i++){
        double x_;
        double y_;
        temp4->GetPoint(i,x_,y_);
        if(i==0) first_4 = xt_first; 
        	temp4->SetPoint(i,(x_-first_4)/60.,y_);
        if( maxX < (x_-first_4)/60.) maxX = (x_-first_4)/60.;
    }
    for(int i=0;i<temp5->GetN();i++){
        double x_;
        double y_;
        temp5->GetPoint(i,x_,y_);
        if(i==0) first_5 = xt_first;
        temp5->SetPoint(i,(x_-first_5)/60.,y_);
        if(maxX< (x_-first_5)/60.) maxX = (x_-first_5)/60.;
    }
    for(int i=0;i<temp2->GetN();i++){
        double x_;
        double y_;
        temp2->GetPoint(i,x_,y_);
        if(i==0) first_2 = xt_first;
        temp2->SetPoint(i,(x_-first_2)/60.,y_);
        if(maxX< (x_-first_2)/60.) maxX = (x_-first_2)/60.;
    }
    for(int i=0;i<temp1->GetN();i++){
        double xd_;
        double yd_;
        temp1->GetPoint(i,xd_,yd_);
        if(i==0) first_1 = xt_first;
        temp1->SetPoint(i,(xd_-first_1)/60.,yd_);
        if(maxX< (xd_-first_1)/60.) maxX = (xd_-first_1)/60.;
    }

    c1->SetGridx(1);
    c1->SetGridy(1);
    temp->SetMarkerStyle(22);
    temp->SetMarkerSize(MarkerSize_);
    temp->SetMarkerColor(kBlue-2);
    temp->SetTitle("4 loads of 3W each + Air Flow (2.5 L/min)");
    temp->SetTitle("");
    temp->GetXaxis()->SetTitle("Time [min]");
    temp->GetYaxis()->SetTitle("Temperature [^{o}C]");
    temp->GetYaxis()->SetRangeUser(-25,0);
    temp->GetXaxis()->SetRangeUser(0,maxX);
    temp->Draw("AP");

    //temp3->SetMarkerStyle(22);
    //temp3->SetMarkerSize(MarkerSize_);
    //temp3->SetMarkerColor(2);
    //temp3->GetXaxis()->SetRangeUser(0,maxX);
    //temp3->Draw("same, eP*");

    temp4->SetMarkerStyle(22);
    temp4->SetMarkerSize(MarkerSize_);
    temp4->SetMarkerColor(kOrange);
    temp4->GetXaxis()->SetRangeUser(0,maxX);
    temp4->Draw("same, eP*");

    temp1->SetMarkerStyle(22);
    temp1->SetMarkerSize(MarkerSize_);
    temp1->SetMarkerColor(kGreen-2);
    temp1->GetXaxis()->SetRangeUser(0,maxX);
    temp1->Draw("same, eP");

    temp5->SetMarkerStyle(22);
    temp5->SetMarkerSize(MarkerSize_);
    temp5->SetMarkerColor(kRed-2);
    temp5->GetXaxis()->SetRangeUser(0,maxX);

    temp2->SetMarkerStyle(22);
    temp2->SetMarkerSize(MarkerSize_);
    temp2->SetMarkerColor(46);
    temp2->GetXaxis()->SetRangeUser(0,maxX);
    temp2->Draw("same, eP");

    //TLine *line = new TLine(minX,-20, maxX,-20);
    //line->SetLineColor(kYellow-2);
    //line->SetLineStyle(2);
    //line->SetLineWidth(4);
    //line->Draw();

    TLegend *legend_nm = new TLegend(0.52,0.74,0.7,0.9);
    legend_nm->SetBorderSize(0);
    legend_nm->SetFillColor(0);
    legend_nm->SetFillStyle(0);
    legend_nm->SetNColumns(1);
    legend_nm->SetTextSize(0.035);
    legend_nm->SetTextSizePixels(25);

    legend_nm->AddEntry(temp,"JUMO, PT100", "p" );
    legend_nm->AddEntry(temp1,"PT1000, On adaptor", "p" );
    legend_nm->AddEntry(temp2,"PT1000, On Al", "p" );
    legend_nm->AddEntry(temp4,"PT1000, Sensor", "p" );
    legend_nm->Draw();

    c1->SaveAs("performance_FOLDER_4pt1000.png");
}

// http://en.wikipedia.org/wiki/Dew_point
float rm(float T, float RH){
    return log( (RH/100.) * exp((b_-T/d_)*(T/(c_+T)))  );  
}

