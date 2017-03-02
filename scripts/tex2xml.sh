#!/bin/bash

tar_path=/data/arXiv_Src_1504_1702/*
sorsa_path=/data/arXiv-

for tarzan in $tar_path; do
    yy=$(echo $tarzan|cut -d_ -f6|cut -c1-2)
    src_yy=$sorsa_path$a
     
    if [ ! -d $src_yy ]; then
        mkdir $src_yy
    fi
    
    echo  extracting $tarzan to $src_yy
    
    tar xf $tarzan -C $src_yy

    for month in $src_yy/*; do
        echo $a $month
        yes n|gunzip $month/*.gz
        for doc in $month/*; do
            if [[ $(file $doc) == *"TeX"* ]]; then
                latexml --destination==$doc.xml $doc 2>&1 |grep -q Fatal >> /home/evly/bigdata/latexml_errors.txt
            fi
        done
#        for gunzipp in $month; do
#            echo extracting $gunzipp
#            yes n|gunzip $gunzipp
#        done
    done
done
