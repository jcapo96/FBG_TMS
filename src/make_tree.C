#include<fstream>
#include<sstream>
#include<stdio.h>
//#include"DataPackage.h"

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

TTimeStamp ConvertTime(unsigned long long int TimeStamp)
{
  TTimeStamp start(1900,1,1,0,0,0);
  TTimeStamp time; time.SetSec(start.GetSec() + 1.0*TimeStamp/1.0e9); cout << start.GetSec() << endl;
  return time;
}

class RunLoader_t
{
   string fname;
public:
   std::ifstream ifs;
   public:

   int PacketSize;
   unsigned long long int TimeStamp;
   int Reserved;
   int ChannelNo;
   int FibreNo;
   double StartWL;
   double StopWL;
   int NPoints;
   std::vector<short> Data;
   bool debug=false;

   public:

   RunLoader_t(char const* path) : ifs(path)
   {

     cout << "Loading " << fname << endl;
//     ifs=std::ifstream(fname, ios::binary );
     ifs.seekg(0);
   }

   RunLoader_t(std::string const& s) : RunLoader_t(s.c_str())
   {

   }
//   RunLoader_t(string s) : ifs(s)
//   {

  // }
   void Print()
   {
      cout << "PacketSize: " << PacketSize << endl;
      cout << "TimeStamp: " << TimeStamp << " " << ConvertTime(TimeStamp).AsString() << endl;
      cout << "Reserved: " << Reserved << endl;
      cout << "ChannelNo: " << ChannelNo << endl;
      cout << "FibreNo: " << FibreNo << endl;
      cout << "StartWL: " << StartWL << endl;
      cout << "StopWL: " << StopWL << endl;
      cout << "NPoints: " << NPoints << endl;
   }
   
   void ReadEvent()
   {
//   DataPackage aa;
//   cout << "SizeOfDataPackage: " << sizeof(DataPackage) << endl;
//     ifs.read( (char*)&aa, 48); aa.Print(); lets_pause();
//     cout << aa.PacketSize << endl;
     ifs.read( (char*)&PacketSize, sizeof(PacketSize)); if (debug) cout << "PacketSize("<<sizeof(PacketSize)<<"): " << PacketSize << endl;
     ifs.read( (char*)&TimeStamp, sizeof(TimeStamp));   if (debug) cout << "TimeStamp("<<sizeof(TimeStamp)<<"):" << TimeStamp << endl; // TimeStamp is not UNIX!!
     ifs.read( (char*)&Reserved, sizeof(Reserved));     if (debug) cout << "Reserved("<< sizeof(Reserved) << "): " << Reserved << endl;
     ifs.read( (char*)&ChannelNo, sizeof(ChannelNo));   if (debug) cout << "ChannelNo("<< sizeof(ChannelNo) << "): " << ChannelNo << endl;
     ifs.read( (char*)&FibreNo, sizeof(FibreNo));       if (debug) cout << "FibreNo("<< sizeof(FibreNo) << "): " << FibreNo << endl;
     ifs.read( (char*)&StartWL, sizeof(StartWL));       if (debug) cout << "StartWL("<< sizeof(StartWL) << "): " << StartWL << endl;
     ifs.read( (char*)&StopWL, sizeof(StopWL));         if (debug) cout << "StopWL("<< sizeof(StopWL) << "): " << StopWL << endl;
     ifs.read( (char*)&NPoints, sizeof(NPoints));       if (debug) cout << "NPoints("<< sizeof(NPoints) << "): " << NPoints << endl;
   
     Data.resize(NPoints);
     ifs.read( (char*)&Data[0], sizeof(Data[0])*NPoints);

     if (debug) for (int i=0; i<5;i++)
     {
        cout << "Data("<< sizeof(Data[i]) << "): " << Data[i] << endl;
     }
   }
   TH1F* GetHist()
   {
     TH1F *hist = new TH1F("h","h",NPoints,StartWL,StopWL);
     for (int i=0; i<NPoints;i++) hist->SetBinContent(i+1,Data[i]);
     return hist;
   }
   void Dump()
   {
     ofstream ofs("spectrum.dump");
     for (int i=0; i<NPoints;i++) ofs << Data[i] << endl; // -> Check file, spectrum is empty! 
   }
   void WriteEvent(std::ofstream &ofs)
   {
     ofs.write((char*)&PacketSize,sizeof(PacketSize));
     ofs.write((char*)&TimeStamp,sizeof(TimeStamp));
     ofs.write((char*)&Reserved,sizeof(Reserved));
     ofs.write((char*)&ChannelNo,sizeof(ChannelNo));
     ofs.write((char*)&FibreNo,sizeof(FibreNo));
     ofs.write((char*)&StartWL,sizeof(StartWL));
     ofs.write((char*)&StopWL,sizeof(StopWL));
     ofs.write((char*)&NPoints,sizeof(NPoints)); 
     ofs.write((char*)&Data[0],sizeof(Data[0])*NPoints); 
   }
   void DumpToBinaryFile( string ofn, std::vector<std::pair<int,int>> Selection)
   {
     ofstream ofs(ofn,ios::binary);
     ReadEvent();
     while(!ifs.eof())
     {
        for(auto p : Selection) if (p.first==ChannelNo && p.second==FibreNo)
        {
          WriteEvent(ofs);
          //cout << p.first << " " << ChannelNo << " " << p.second <<  " " <<FibreNo << endl;GetHist()->Draw("HIST SAME");  lets_pause();
        }
        ReadEvent();

     }
     ofs.close();
   }
};
void make_tree(string filename)
{
   if(0)
   {
    //string filename="/eos/user/j/jcapotor/FBGdata/Data/Heater_Tests/09012023/09012023_spectrum_1.txt";
    std::vector<std::pair<int,int>> Selection({{0,0}}); //List of Channel&Fibre selection to save in the reduced file.
    RunLoader_t run(filename);   
    run.DumpToBinaryFile(Form("%s_cut.bit",filename.c_str()),Selection);
   }
   if(1)
   {
   // string filename="myfile.bin";
    RunLoader_t run(filename);   

    //Now we read the new file to check it is fine.
    TCanvas *c = new TCanvas("c");
    for(int i=0;i<1000;i++)
    {
      run.ReadEvent();
      c->cd();
      run.GetHist()->Draw("HIST SAME");      run.Print(); lets_pause();
    }
   } 

}
