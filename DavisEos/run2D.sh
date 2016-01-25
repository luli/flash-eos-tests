#!/bin/bash

#export EOS_TEST=DG2

mkdir -p  build
cp setup/flash4 build/
rm -f frun_${EOS_TEST}_2D/*
flmake run -t frun_${EOS_TEST}_2D -n 2
#python yt-viz/analyse_vdw.py
