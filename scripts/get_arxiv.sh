#!/bin/bash

yy=15
mm=4
zero=0

while [ $yy -le 17 ]; do
    while [ $mm -le 12 ]; do
        s3cmd get -v --stop-on-error --requester-pays s3://arxiv/src/arXiv_src_$yy$zero$mm* /data/arXiv_Src_1504_1702/
        let mm=$mm+1        
        if [ $mm -ge 10 ]; then
            unset zero
        fi
    done
    let zero=0
    let mm=0
    let yy=$yy+1
done
