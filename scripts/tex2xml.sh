#!/bin/bash

check(){
    local pid=$1
    waited=0

    while [ -d /proc/$pid ] ; do
        if [ "$(ps -F ${pid}|tr -s ' '|cut -d ' ' -f6|tail -n1)" -gt "3000000" ] || [ $waited -gt "300" ]; then 
            printf $doc"\nkilled\n" >> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
            kill -9 ${pid}
            return
        else 
            sleep 30
            waited=$(($waited+30))
        fi
    done
} 

tar_path=/data/arXiv_Src_1504_1702/arXiv_src_1701_*
sorsa_path=/data/pulp/latexml/arXiv-

rm /home/evly/tmt/bigdata/latexml_errors.txt /home/evly/tmt/bigdata/latexml_fatalerrors.txt
rm -r ${sorsa_path}{17,17-src}

if [ ! -d "${sorsa_path}" ]; then
        mkdir -p ${sorsa_path}
    fi

for tarzan in ${tar_path}; do
    # get year of tarball
    yy=$(echo ${tarzan}|cut -d'_' -f6|cut -c1-2)
    src_yy=${sorsa_path}${yy}
    echo sorsa ja vuosi ${src_yy}

    # create folders per year for source files
    if [ ! -d ${src_yy} ]; then
        mkdir ${src_yy} ${src_yy}-src
    fi
    
    echo  extracting ${tarzan} to ${src_yy}-src
    tar xf ${tarzan} -C ${src_yy}-src
#    cp ${src_yy}-zipped ${src_yy}-zipped_copy

    # extract gziped files
    for month in ${src_yy}-src/*; do
        mm=$(echo ${month}|cut -d'/' -f6)

        src_mm=${src_yy}/${mm}
        echo parsing ${month} : year ${yy} and month ${mm} and together ${src_mm}

        echo extracting gzip files from ${month}
        yes n|gunzip ${month}/*.gz
        
        echo creating folder for pdf files to ${src_mm}/pdfss and transfering pdf files
        mkdir -p mkdir ${src_mm}/pdfss
        mv ${month}/*.pdf ${src_mm}/pdfss/

        for doc in ${month}/*; do
            # transform latex files to xml and move to source folder
            if [[ $(file ${doc}) == *"TeX"* ]]; then
                echo tex file found: ${doc}
#                arxiv_id=$(echo ${doc} | cut -d'/' -f6)            
#                echo arXiv id ${arxiv_id}

                latexml --includestyles ${doc} > ${doc}.xml 2> /home/evly/tmt/bigdata/latexml_errors.txt & pid=$!
                check $pid 
                 
                fatal=$(grep -q fatal /home/evly/tmt/bigdata/latexml_errors.txt)
                if [ -n "$fatal" ]; then
                    echo "fatal error found"
                    printf $doc"\n"$fatal"\n" >> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
                fi

                mv ${doc}.xml ${src_mm}/

            # get folders and untar
            elif [[ $(file $doc) == *"POSIX"* ]]; then
                echo "tar file found: ${doc}"

                mv ${doc} ${doc}.tar && mkdir ${doc} && tar xf ${doc}.tar -C ${doc}

                # latex to xml and move to source folder
                for d in ${doc}/*; do
#                    if [[ $(file ${d}) == *"TeX"* ]]; then
                    if [ ${d: -3} == "tex" ]; then
                        echo "tex file found: ${d}"
                        latexml --includestyles "${d}" > "${d}".xml 2> /home/evly/tmt/bigdata/latexml_errors.txt & pid=$!
                        check $pid

                        fatal=$(grep -q fatal /home/evly/tmt/bigdata/latexml_errors.txt)
                        if [ -n "$fatal" ]; then
                            echo "fatal error found"
                            printf $doc"\n"$fatal"\n" >> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
                        fi
                    fi
                done

                mv ${doc} ${src_mm}/
            fi
        done
    done
done
