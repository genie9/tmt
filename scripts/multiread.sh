#qqqq)!/bin/bash

path_xml="/data/arXiv-??/*/"
path_meta="/home/evly/tmt/bigdata/arxiv_meta"
path_years="/home/evly/tmt/bigdata/arxiv_years"
path_mallet="/data/mallet_tests/arXiv_cs/"

 
# go through files with id and make soft links to $path_mallet
for f in $(ls $path_meta); do
    i=0
    for id in $(cut -d '"' -f4 $f); do
        echo "found id "$id
        path_id=find $path_xml$id -type d
        if [ -d $path_id ]; then
            echo "found path "$path_id
            find $path_id -name "*.xml"
            #i=$((i+1))
        else
            echo "found file"
            find $path_xml -name "$id.xml" 
            #i=$((i+1))
        fi
    done
    echo "1000 entrys processed in "$f
done

echo "done"

find /data/arXiv-??/*/ -maxdepth 3 -mindepth 1  >> /home/evly/tmt/bigdata/find.txt

#for d in $(ls $path_xml); do
     
 #   find $path_xml -path *$tmp* -prune -exec find {} -name *.xml \; | sudo rsync -avz --progress  $i /data/mallet_tests/ \;
#done

#for i in $(ls $path); do
 #   sudo rsync -avz --progress $path$i /data/mallet_tests/ \;
#done 
#for i in $(ls $path); do
 #   sudo rsync -avz --progress $i /data/mallet_tests/ \;
#done

#find $path$i -path *cs*/*.xml -exec 
#FIND $PATH -path */cs* -type d -prune -exec find {} -name *.xml \;
