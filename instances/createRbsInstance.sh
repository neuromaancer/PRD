#!/bin/bash
# author: Alafate ABULIMITI

for i in *.txt
do
    wine RBS_FLOWSHOP.exe $i > $i.out
    cp ub.rep $i.rbs
done