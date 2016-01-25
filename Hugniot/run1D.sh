#!/bin/bash
mkdir -p  build
cp setup/flash4 build/
#set -x
#export EOS_TABLE='Al_feos_83719_eoffset_1'
export EOS_TABLE='al-imx-003'

rm -v yt-viz/hugoniot_${EOS_TABLE}.h5
rm -f yt-viz/out/${EOS_TABLE}/*
for idx in 5 10 20 35 50 75 100 150 250 350
do
    echo $idx
    export SOURCE_TEMP=$idx
    rm -f ./frun_${SOURCE_TEMP}/*
    mkdir -p frun_${SOURCE_TEMP}
    cp simulations/Hugoniot/${EOS_TABLE}.cn4 frun_${SOURCE_TEMP}/
    flmake run -t frun_${SOURCE_TEMP} > frun_${SOURCE_TEMP}/stdout.log
    EOS_TABLE=$EOS_TABLE SOURCE_TEMP=$idx python yt-viz/analyse_shock_tube.py &
done
