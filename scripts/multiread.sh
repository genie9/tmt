#!/bin/bash



#ssh -A -t evly@shell.hiit.fi ssh -A ugluk.hiit.fi 'find /data/ -type f -name cs*.xml -print0 |xargs -I% -0 rsync -aPvhze "ssh -A -t evly@shell.hiit.fi ssh -A ugluk.hiit.fi" :% /home/evly/arxiv/ |grep -v /$'
 
#rsync -avhzPe "ssh -A -t evly@shell.hiit.fi ssh -A ugluk.hiit.fi" --files-from =< (find /data/ -type f -name cs*.xml) python/|grep -v /$

#find /data/ -type f -name cs*.xml -exec rsync -avz --progress /home/evly/tmt/text/ \;

path="/data/arXiv-*/*/cs*/"

for i in $(ls $path); do
    sudo rsync -avz --progress $i /data/mallet_tests/ \;
done

for i in $(ls $path); do
    sudo rsync -avz --progress $path$i /data/mallet_tests/ \;
done 

#find $path$i -path *cs*/*.xml -exec 
find /data/arXiv-?? -path */cs* -type d -prune -exec find {} -name *.xml \;
