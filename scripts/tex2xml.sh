#!/bin/bash

check(){
    local pid=$1
    time_el=0

    while [ -d /proc/$pid ] ; do
        mem="$(ps -F ${pid}|tr -s ' '|cut -d ' ' -f6|tail -n1)"
        if [ $mem -gt "3000000" ]; then 
            kill -9 ${pid}
#            if [[ $? == 0 ]]; then
            echo -e $doc'\tkilled, memory' >> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
            return
#            else
#            fi
        elif [ $time_el -gt "300" ]; then 
            kill -9 ${pid}
            echo -e $doc'\tkilled, time'>> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
            return
        else 
            sleep 30
            time_el=$(($time_el+30))
        fi
    done
} 

fatal(){
    local doc=$1

    fatal=$(grep -q fatal /home/evly/tmt/bigdata/latexml_errors.txt)
    if [ -n "$fatal" ]; then
        echo "fatal error found"
        echo -e $doc'\t'$fatal >> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
    fi
}

process() {
    local doc=$1
    local done_mm=$2

    # transform latex files to xml and move to source folder
    if [[ $(file ${doc}) == *"TeX"* ]]; then
        echo tex file found: ${doc}

        latexml --includestyles ${doc} > ${doc}.xml 2> /home/evly/tmt/bigdata/latexml_errors.txt & pid=$!
        check $pid 
        fatal $doc                 
        mv ${doc}.xml ${done_mm}/ && rm ${doc}

    # get folders and untar
    elif [[ $(file $doc) == *"POSIX"* ]]; then
        echo "tar file found: ${doc}"

        mv ${doc} ${doc}.tar && mkdir ${doc} && tar xf ${doc}.tar -C ${doc} && rm ${doc}.tar

        # latex to xml and move to source folder
        for d in ${doc}/*; do
#                    if [[ $(file ${d}) == *"TeX"* ]]; then
            if [ ${d: -3} == "tex" ]; then
                echo "tex file found: ${d}"
                latexml --includestyles "${d}" > "${d}".xml 2> /home/evly/tmt/bigdata/latexml_errors.txt & pid=$!
                check $pid
                fatal $doc
            fi
        done

        mv ${doc} ${done_mm}/ 

    elif [[ $(file ${doc}) == *": data"* ]]; then
        echo data file found: ${doc}

        latexml --includestyles ${doc} > ${doc}.xml 2> /home/evly/tmt/bigdata/latexml_errors.txt & pid=$!
        check $pid 
        fatal $doc                 
        mv ${doc}.xml ${done_mm}/ && rm ${doc}

    else
        echo -e $doc'\t'$(echo $(file $doc)|cut -d':' -f2) >> /home/evly/tmt/bigdata/latexml_fatalerrors.txt
        mv $doc ${done_mm}/nonxml/
    fi
}


tar_path=/data/arXiv_Src_1504_1702
sorsa_path=/data/arXiv-
mkfifo tmp_fifo

counter=0

#rm /home/evly/tmt/bigdata/latexml_errors.txt /home/evly/tmt/bigdata/latexml_fatalerrors.txt
rm -rf ${sorsa_path}15-src/1505

if [ ! -d "${sorsa_path}" ]; then
        mkdir -p ${sorsa_path}
    fi

for tarzan in ${tar_path}/*; do
    # get year of tarball
    mm=$(echo ${tarzan}|cut -d'_' -f6) 
    echo "tarball's month $mm"

    if [ $mm -ne "1504" ]; then
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

        for doc in ${src_mm}/*; do
            arxiv_id=$(echo ${doc} | cut -d'/' -f5)            
            echo arXiv id ${arxiv_id}

            if [ -e ${done_mm}/${arxiv_id}.xml ] || [ -e  ${done_mm}/${arxiv_id}/ ]; then
                echo "file $doc exists"
                rm $doc
            else
                echo "processing $doc, count $counter"
                
                if [ $counter -lt 10 ]; then # we are under the limit
                    { process $doc $done_mm; echo 'done' > tmp_fifo; } &
                    let $[counter++];
                else
                    read x < tmp_fifo # waiting for a process to finish
                    { process $doc $done_mm; echo 'done' > tmp_fifo; } &
                fi
            fi
        done
        if [ $counter -gt 0 ]; then
            cat tmp_fifo > /dev/null # let all the background processes end
            counter=0
        fi
    fi
done

rm tmp_fifo
