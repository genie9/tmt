#!/bin/bash


tar_path=/data/arXiv_Src_1504_1702
sorsa_path=/data/arXiv-

#rm /home/evly/tmt/bigdata/latexml_errors.txt /home/evly/tmt/bigdata/latexml_fatalerrors.txt
# delete month if needed to process again
#rm -rf ${sorsa_path}15-src/1508/ 

if [ ! -d "${sorsa_path}" ]; then
        mkdir -p ${sorsa_path}
    fi

for tarzan in ${tar_path}/*; do
    # get year of tarball
    mm=$(echo ${tarzan}|cut -d'_' -f6) 
    echo "tarball's month $mm"

    if ! [[ $mm =~ ^(15[0-9]*) ]]; then # change conditions for month not to be included in processing (e.g. alredy processed ones)
        yy=$(echo ${tarzan}|cut -d'_' -f6|cut -c1-2)
        src_yy=${sorsa_path}${yy}
        echo sorsa ja vuosi ${src_yy}
        src_mm=${src_yy}-src/${mm}
        done_mm=${src_yy}/${mm}
        echo "sorsa ${src_mm}, done ${done_mm}"

        echo creating folders per year and month for source and files
        if [ ! -d ${src_mm} ] && [ ! -d ${done_mm} ]; then
            mkdir -p ${src_mm} ${done_mm}/pdfss ${done_mm}/nonxml
        fi
        
        echo  extracting ${tarzan} to ${src_yy}-src
        tar xf ${tarzan} -C ${src_yy}-src

        echo extracting gzip files from ${src_mm}
        gunzip ${src_mm}/*.gz
        
        echo transfering pdf files
        mv ${src_mm}/*.pdf ${done_mm}/pdfss/
#---------------------------------------------------------
        find ${src_mm} -maxdepth 1 -mindepth 1 | xargs -P 10 -I {} /home/evly/process.sh {} $done_mm
#------------------------------------------------------------
    fi
done
