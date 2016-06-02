#!/bin/bash



#ssh -A -t evly@shell.hiit.fi ssh -A ugluk.hiit.fi 'find /data/ -type f -name cs*.xml -print0 |xargs -I% -0 rsync -aPvhze "ssh -A -t evly@shell.hiit.fi ssh -A ugluk.hiit.fi" :% /home/evly/arxiv/ |grep -v /$'
 
#rsync -avhzPe "ssh -A -t evly@shell.hiit.fi ssh -A ugluk.hiit.fi" --files-from =< (find /data/ -type f -name cs*.xml) python/|grep -v /$

