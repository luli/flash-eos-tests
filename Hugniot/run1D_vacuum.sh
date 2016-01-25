#!/bin/bash
mkdir -p  build
cp setup/flash4 build/
#set -x
export EOS_TABLE='Al_feos_83719_eoffset_1'
#export EOS_TABLE='al-imx-003'

rm -f yt-viz/out/vacuum/*
rm -f ./frun_vacuum/*
mkdir -p frun_vacuum
cp simulations/Hugoniot/${EOS_TABLE}.cn4 frun_vacuum/
EOS_TABLE=$EOS_TABLE flmake run --rc flashrc_vacuum.py -t frun_vacuum #> frun_vacuum/stdout.log
