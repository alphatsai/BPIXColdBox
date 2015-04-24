#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <stdio.h>
#define MAXPOINTS 1000;

void BMTest_IV(const char iv_file[100], char ModType[100], int ModN)
{
 
  Int_t ModN;
  Char_t ModType[100];
  Float_t fnorm;
  Float_t V[MAXPOINTS];
  Float_t I[MAXPOINTS]; 
  Float_t Vabs[MAXPOINTS];
  Float_t Iabs[MAXPOINTS]; 
  Int_t num;
  std::cout<<"Bare Module Test"<<std::endl;
    Int_t ncol;
  std::cout<<"****** IV measurement *******"<<std::endl;
  std::cout<<"****************************"<<std::endl;
  std::cout<<"Loading Data..."<<std::endl;
 
  FILE *fb = fopen(iv_file,"r");

  
  int i = 0;
     
  while(1){

      ncol=fscanf(fb,"%f %f",&V[i],&I[i]);
    
      std::cout<<V[i]<<"  ,   "<<I[i]<<std::endl;
      if(ncol<0) break;
      i++;         
  }
	
	int n=i;	
	std::cout<<"There is "<<n<<" measures"<<std::endl;
  std::cout<<"Done."<<std::endl;

   
  fclose(fb);
  /////////////////////////////////////////////////////////


  TCanvas *c1 = new TCanvas("c1","",300,300,600,700);
	c1->Divide(1,2);
  c1_1->cd();
  c1->SetFillColor(0);
  c1->SetGrid();
  c1->GetFrame()->SetFillColor(21);
  c1->GetFrame()->SetBorderSize(12);
 
  
   for(Int_t t=0;t<n;t++){
     
     //Iabs[t]=fabs(I[t]/1.0e-6);
     //Vabs[t]=fabs(V[t]);
     Iabs[t]=fabs(I[t]);
     Vabs[t]=fabs(V[t]);
     cout<<"("<<Vabs[t]<<" , "<<Iabs[t]<<")"<<endl;
       
   }
   
   //cout<<"Init parameters: ("<<P0_init<<","<<P1_init<<","<<P2_init<<")"<<endl;
   TF1 *func = new TF1("func","pol1",50.,200);
   gStyle->SetOptFit(01111);//Para que te salgan los parametros en el canvas
   func->SetParameters(0,1);
   func->SetParName(1,"slope");
   func->SetParName(0,"intercept");
   
	
	 TGraph *gr = new TGraph(n,Vabs,Iabs);
	 TString title = Form("%s Module %i", ModType, ModN);
	 //cout << ModType2<<endl;
	 gr->SetTitle(title); 
	 gr->SetMarkerColor(4);
	 gr->SetMarkerStyle(21);
	 gr->GetXaxis()->SetTitle("V [V]");
	 gr->GetYaxis()->SetTitle("I [uA]");
	 gr->GetXaxis()->SetTitleSize(0.05);
	 gr->GetYaxis()->SetTitleSize(0.05);
	 gr->GetXaxis()->SetLabelSize(0.05);
	 gr->GetYaxis()->SetLabelSize(0.05);
	 //gr->Fit(func,"","",70,240);
	 gr->Draw("AL*");
	 c1_1->SaveAs(Form("%s_Module%i_IV.gif", ModType, ModN));

	c1_2->cd();
   
	TGraph *grz = new TGraph(n,Vabs,Iabs);
	//grz->SetTitle("Module{ID}"); //a–adir el nombre del m—dulo; ver Scripts.
	grz->SetMarkerColor(4);
	grz->SetMarkerStyle(21);
	grz->GetXaxis()->SetTitle("V [V]");
	grz->GetYaxis()->SetTitle("I [uA]");
	grz->GetXaxis()->SetTitleSize(0.05);
	grz->GetYaxis()->SetTitleSize(0.05);
	grz->GetXaxis()->SetLabelSize(0.05);
	grz->GetYaxis()->SetLabelSize(0.05);
	grz->GetYaxis()->SetRangeUser(0,5);
	grz->Draw("AL*");
	c1_2->SaveAs(Form("%s_Module%i_IV_zoom.gif", ModType, ModN));
	
  

}


