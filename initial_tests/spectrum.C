#include<fstream>
#include<sstream>
#include<stdio.h>


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

class RunLoader_t
{
   string fname;
   ifstream ifs;

   int PacketSize;
   unsigned long long int TimeStamp;
   int Reserved;
   int ChannelNo;
   int FibreNo;
   double StartWL;
   double StopWL;
   int NPoints;
   std::vector<short> Data;

   public:
   RunLoader_t(string s) : fname(s)
   {
     cout << "Loading " << fname << endl;
     ifs=ifstream(fname, ios::binary );
     ifs.seekg(0);

   }
   void ReadEvent()
   {
   
     ifs.read( (char*)&PacketSize, sizeof(PacketSize)); cout << "PacketSize("<<sizeof(PacketSize)<<"): " << PacketSize << endl;
     ifs.read( (char*)&TimeStamp, sizeof(TimeStamp));   cout << "TimeStamp("<<sizeof(TimeStamp)<<"):" << TimeStamp << endl; // TimeStamp is not UNIX!!
     ifs.read( (char*)&Reserved, sizeof(Reserved));     cout << "Reserved("<< sizeof(Reserved) << "): " << Reserved << endl;
     ifs.read( (char*)&ChannelNo, sizeof(ChannelNo));   cout << "ChannelNo("<< sizeof(ChannelNo) << "): " << ChannelNo << endl;
     ifs.read( (char*)&FibreNo, sizeof(FibreNo));       cout << "FibreNo("<< sizeof(FibreNo) << "): " << FibreNo << endl;
     ifs.read( (char*)&StartWL, sizeof(StartWL));       cout << "StartWL("<< sizeof(StartWL) << "): " << StartWL << endl;
     ifs.read( (char*)&StopWL, sizeof(StopWL));         cout << "StopWL("<< sizeof(StopWL) << "): " << StopWL << endl;
     ifs.read( (char*)&NPoints, sizeof(NPoints));       cout << "NPoints("<< sizeof(NPoints) << "): " << NPoints << endl;
   
     Data.resize(NPoints);
     ifs.read( (char*)&Data[0], sizeof(Data[0])*NPoints);

     for (int i=0; i<5;i++)
     {
        cout << "Data("<< sizeof(Data[i]) << "): " << Data[i] << endl;
     }
   
     Draw();
     Dump();
   }
   void Draw()
   {
     TH1F hist("h","h",NPoints,StartWL,StopWL);
     for (int i=0; i<NPoints;i++) hist.SetBinContent(i+1,Data[i]);
     hist.Draw("HIST");
     lets_pause();
   }
   void Dump()
   {
     ofstream ofs("spectrum.dump");
     for (int i=0; i<NPoints;i++) ofs << Data[i] << endl; // -> Check file, spectrum is empty! 
   }
};
void spectrum()
{
   string filename="/Users/jcapo/Documents/FBGS/Data/InterrogatorTests/20221222/11_spectrum_OPTICS.txt";
   RunLoader_t run(filename);

   for(int i=0;i<100;i++) run.ReadEvent(); 

}