#!/bin/bash
export Variable=$1
echo "Processing $Variable"
# source /afs/cern.ch/user/j/jcapotor/FBGana/venv/bin/activate
cp /afs/cern.ch/user/j/jcapotor/FBGana/src/make_tree.py .
python3 make_tree.py $Variable