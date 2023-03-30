#include<fstream>
#include<iostream>
void lets_pause (){
	TTimer * timer = new TTimer("gSystem->ProcessEvents();", 50, kFALSE);
	timer->TurnOn();
	timer->Reset();
	std::cout << "q/Q to quit, other to continuee: ";
	char kkey;
	std::cin.get(kkey);
	if( kkey == 'q' || kkey == 'Q') 			 throw std::exception(); //std::exit(0); //gSystem->Exit(0); //
	timer->TurnOff();
	delete timer;
}
class Evt_t
{
    public:
    long int time; string stime; float time_seconds;
    std::pair<double,double> wvl[8];
    void Print()
    {
        cout << "Time: " << time << "\t" << stime << "\t" << time_seconds << endl;
        for(int k=0; k<8; k++) cout << wvl[k]. first << " " << wvl[k].second << endl;
    }
    void SetStime(string st)
    {
//        cout << st << endl;
//        cout << st.substr(6,st.length()-6) << endl;
        int Hour=stoi(st.substr(0,2));
        int Minute=stoi(st.substr(3,2));
        float Seconds=stof(st.substr(6,st.length()-6));
        time_seconds=Hour*3600+Minute*60+Seconds;
//        cout << st << " = " << Hour << " " << Minute <<  " " << Seconds << " " << time_seconds <<  endl;
//        cout << endl; lets_pause();
    }
};
void FBG()
{
   //string fname="fbg_optics11_wl.txt";
   //string fname_rtd="rtd_temp_1.txt";
   string fname="/Users/jcapo/Documents/FBGS/Data/Initial_Tests/fbg_optics11_wl_ice_2.txt";
   string fname_rtd="/Users/jcapo/Documents/FBGS/Data/Initial_Tests/rtd_temp_ice_2.txt";
   TFile file("out.root","RECREATE");
   ifstream ifs(fname,ios::in);
   if (!ifs.is_open()) { cout <<"File not opened" << endl;}
   // 5 variables de cabecera
   // 9 variables por canal.
   int NVarPerChannel=9;
   int NColumns=77; int NChannels=8;
   std::vector<string> v(NColumns); //canales (77-5)/9 = 8
   string date, time, nanoseconds, aux, aux2;
   TTree *t = new TTree("FBG","FBG");
   Evt_t ev;
   t->Branch("Time_NS",&(ev.time),"Time_NS/L");
   t->Branch("time_seconds",&ev.time_seconds, "time_seconds/F");
   for (int i=0; i<v.size();i++) ifs >> v[i]; //leemos el primer evento
   for (int i=0; i<v.size();i++) cout << i << " : " << v[i] << endl;
   string varname;
   for(int k=0; k<NChannels;k++)
   {
     varname=Form("CH%s_FB%s_SN%s",v[6+k*NVarPerChannel].c_str(),v[8+k*NVarPerChannel].c_str(),v[10+k*NVarPerChannel].c_str());
     t->Branch(Form("%s_Mean",varname.c_str()),&(ev.wvl[k].first),Form("%s_Mean/D",varname.c_str()));
     t->Branch(Form("%s_STD",varname.c_str()),&(ev.wvl[k].second),Form("%s_STD/D",varname.c_str()));
   }int counter=0;
   while(1)
   {
      for (int i=0; i<v.size();i++) ifs >> v[i];
      if(ifs.eof()) break;
//      for (int i=0; i<v.size();i++) cout << i << " : " << v[i] << endl;
      ev.time=std::stol(v[2]);
      ev.SetStime(v[1]);
      for (int k=0; k<NChannels;k++) {ev.wvl[k].first=std::stod(v[12+k*NVarPerChannel]); }
      for (int k=0; k<NChannels;k++) { ev.wvl[k].second=std::stod(v[13+k*NVarPerChannel]);}
//      ev.Print();lets_pause();
      t->Fill();
   }
   t->Write("FBG");
   ifs.close();
   ifstream ifs_rtd(fname_rtd,ios::in);
   if (!ifs_rtd.is_open()) { cout <<"File not opened" << endl;}
   TTree *t2 = new TTree("RTD","RTD");
   string stime; float time_seconds; double temp1, temp2;
   t2->Branch("time_seconds",&ev.time_seconds,"Time_seconds/F");
   t2->Branch("T1",&(temp1),"T1/D");
   t2->Branch("T2",&(temp2),"T2/D");
   while(1)
   {
      ifs_rtd >> aux >> stime >> temp1 >> temp2;
      if(ifs_rtd.eof()) break;
      ev.SetStime(stime);
      t2->Fill();
   }
   t2->Write("RTD");
   ifs_rtd.close();
   TCanvas *c = new TCanvas("c");
   c->Divide(1,2);
   c->cd(1);
   t->Draw("CH1_FB1_SN1_Mean:time_seconds");
   t->Draw("CH1_FB1_SN2_Mean:time_seconds","SAME");
   t->Draw("CH1_FB1_SN3_Mean:time_seconds","SAME");
   t->Draw("CH1_FB1_SN4_Mean:time_seconds","SAME");
   c->cd(2); t2->Draw("T1:time_seconds");
   lets_pause();
   file.Close();
}