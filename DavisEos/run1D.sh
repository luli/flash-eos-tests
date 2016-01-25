#!/bin/bash

#export EOS_TEST=DG2

mkdir -p  build
cp setup/flash4 build/
rm -f frun_${EOS_TEST}_1D/*
flmake run -t frun_${EOS_TEST}_1D
python yt-viz/analyse_vdw.py
