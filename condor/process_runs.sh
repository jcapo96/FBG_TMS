#!/bin/bash
export Variable=$1
echo "Hola Jordi $Variable"
cp -r /afs/cern.ch/user/j/jcapotor/FBG_TMS/venv
source venv/bin/activate
cp -r /afs/cern.ch/user/j/jcapotor/FBG_TMS/src
cp -r /afs/cern.ch/user/j/jcapotor/FBG_TMS/ana_tools
cd src
python3 process_runs.py $Variable
