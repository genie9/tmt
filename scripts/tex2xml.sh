#!/bin/bash

tar_path=/data/arXiv_Src_1504_1702/*
sorsa_path=/data/arXiv-

for tarzan in $tar_path; do
    # get year of tarball
    yy=$(echo $tarzan|cut -d'_' -f6|cut -c1-2)
    src_yy=$sorsa_path$a
     
    # create folders per year for source files
    if [ ! -d $src_yy ]; then
        mkdir $src_yy $src_yy-src
    fi
    
    echo  extracting $tarzan to $src_yy
    tar xf $tarzan -C $src_yy-src
#    cp $src_yy-zipped $src_yy-zipped_copy

    # extract gziped files
    for month in $src_yy-src/*; do
        echo $a $month
        yes n|gunzip $month/*.gz
        
        mkdir $src_yy/$month/ && mkdir $src_yy/$month/pdfss && mv $src_yy-src/$month/*.pdf $src_yy/$month/pdfss/

        for doc in $month/*; do
            arxiv_id=echo $doc | cut -d'/' -f5
            
            # transform latex files to xml and move to source folder
            if [[ $(file $doc) == *"TeX"* ]]; then
                echo $doc >> /home/evly/bigdata/latexml_errors.txt && latexml --destination==$doc.xml $doc 2>&1 |grep -q Fatal >> /home/evly/bigdata/latexml_errors.txt
                mv $src_yy-src/$month/*.xml $src_yy/$month/

            # get folders and untar
            elif [[ $(file $doc) == *"POSIX"* ]]; then
                mv $doc $doc.tar && mkdir $doc && tar xf $doc.tar -C $doc
                # latex to xml and move to source folder
                for d in $doc/*; do
                    if [[ $(file $doc) == *"TeX"* ]]; then
                        echo $doc >> /home/evly/bigdata/latexml_errors.txt && latexml --destination==$doc.xml $doc 2>&1 |grep -q Fatal >> /home/evly/bigdata/latexml_errors.txt
                        mv $src_yy-src/$month/*.xml $src_yy/$month/
                    fi
                done
            fi
        done

    
#        for gunzipp in $month; do
#            echo extracting $gunzipp
#            yes n|gunzip $gunzipp
#        done
    done
done
