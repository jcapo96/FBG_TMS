#!/bin/bash
export Variable=$1
echo "Hola Jordi $Variable"
source /afs/cern.ch/user/j/jcapotor/FBG_TMS/venv/bin/activate
cp /afs/cern.ch/user/j/jcapotor/FBG_TMS/src/process_runs.py .
python3 process_runs.py $Variable