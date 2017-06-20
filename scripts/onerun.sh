#!/bin/bash

################################################################
############# variables and directory names ####################
################################################################

# make $data_root to be the root of data folder
# here assumption is that we are in tmt repository root
data_root=data/

# from and until indicating the period of data to be processed
from=970101
until=140430
setspec=cs

# minimum length of sections to keep
min_len=50
stem=nonstem # or stem

# numbers to find words to exclude from corpus:
# exclude words which are seen in less than n documents
doc_freq=6
# exclude words which are seen less than n times
word_freq=6
# exclude words which are in more than n % of documents
doc_cov=100
proc=4
# here is root to full arxix raw data set
arxiv_data_root=${data_root}

# folders and files
all_arxiv=${data_root}all_arxiv.txt
data_current=${data_root}${setspec}_${from}_${until}/
arxiv_raw=${data_current}arxiv_raw/
meta_ids=${data_current}meta_ids.txt
paths=${data_current}paths.csv
preproc=${data_current}preproc_${stem}_${min_len}/
corpus=${data_current}corpus_${stem}_${min_len}.csv
junk=${data_current}junk_${stem}_${min_len}.txt
errors=${data_current}errorfiles_${min_len}.txt
final_data=${data_current}to_mallet/

################################################################

# this script is for arxiv bulk download. 
#./scripts/get_arxiv.sh

find ${arxiv_data_root}arXiv-??/*/ -maxdepth 3 -mindepth 1 >> ${all_arxiv}

# finds arXiv identifiers for specific set and dates
# picks up data from http://export.arxiv.org/oai2
python scripts/get_meta2ids.py ${setspec} ${from} ${until} ${meta_ids}
# --> data/cs_1997-01-01_2014-04-30/arxiv_ids_.txt

# uses 'all_arxiv.txt', 'arxiv_ids.txt' 
python scripts/match_files.py ${arxiv_data_root} ${all_arxiv} ${meta_ids} ${paths}

# --> data/cs_1997-01-01_2014-04-30/paths.csv
# catenates xml files from document folder to one xml file without styling
# copies xml files to separate folder for further processing
# uses 'paths.txt'
python scripts/cat_copy_xml.py ${paths} ${arxiv_raw}
# --> data/cs_1997-01-01_2014-04-30/arXiv_raw/*.xml

# Cleanes xml files and produces a folder with preprocessed text files.
# If stemming is desired add 'stem' to the end of the parameter list.
# min_len for abstracts is hard coded in the script to be 10 words.
# Files that has not been preprocessed are written in 'errorfiles_<min_len>.txt'.
# Uses 'arxiv_raw/'
# This is the slowest part of processing, maybe should be multiprocessed from here??
python scripts/xml_clean_combo_abstr.py ${data_current} ${arxiv_raw} ${min_len} ${stem} 
# --> data/cs_1997-01-01_2014-04-30/preproc_nonstem_50/sect/*.txt
# --> data/cs_1997-01-01_2014-04-30/preproc_nonstem_50/full/*.txt
# --> data/cs_1997-01-01_2014-04-30/section_titles_50.txt
# --> data/cs_1997-01-01_2014-04-30/errorfiles_50.txt

# summary of corpus words
# uses preproc_<stem>_<min_len>/full/
python scripts/words_corpus.py ${data_current} ${preproc}full/ ${corpus}
# --> data/cs_1997-01-01_2014-04-30/corpus_nonstem.txt

# finding words to exclude from corpus
# uses corpus_<stem>_<min_len>.csv
python scripts/stopwords.py ${corpus} ${junk} ${doc_freq} ${word_freq} ${doc_cov}
# --> data/cs_1997-01-01_2014-04-30/junkwords_nonstem_50.txt

# produces final text for topic modelling
python scripts/final_preproc.py ${preproc} ${data_current}to_mallet/ ${junk} ${errors} 
# min_len hardcoded !!!!


################# topic modelling with MALLET #######################

# variables
topics=100
threads=8

# files and folders
mallet=${data_current}mallet/
import_sec=${mallet}sections_${stem}.mallet
import_full_pipe=${mallet}full_${stem}_pipe.mallet
topics_path=${mallet}topics${topics}/
topics_sect=${topics_path}sect/
topics_full=${topics_path}full_infered/
inferencer=${topics_path}sections.inferencer

mkdir -p ${topics_full} ${topics_sect}

mallet/bin/mallet import-dir \
    --input ${final_data}sect \
    --output ${import_sec} \
    --keep-sequence

mallet/bin/mallet import-dir \
    --input ${final_data}full \
    --output ${import_full_pipe} \
    --use-pipe-from ${import_sec} \
    --keep-sequence

mallet/bin/mallet train-topics \
    --input ${import_sec} \
    --num-topics ${topics} \
    --num-threads ${threads} \
    --output-topic-keys ${topics_sect}keys.txt \
    --output-doc-topics ${topics_sect}composition.txt \
    --inferencer-filename ${inferencer}

mallet/bin/mallet infer-topics \
    --inferencer ${inferencer} \
    --input ${import_full_pipe}\
    --output-doc-topics ${topics_full}composition.txt


############ processing mallet and arxiv data for pulp ##############

# files and folders
#shared_ids.txt
keys_uniq=${topics_sect}keys_uniq.txt
full_texts=${topics_sect}texts_nonstem_50.txt
topic_nums=${topics_sect}topic_summary_nonstem_nums.txt

# Cleans non stemmed keys from obvious similarities
# 'keys_uniq.txt' is used in pulp db building
if [[ ${stem} == 'nonstem' ]]; then
    python scripts/keys.py ${topics_sect}keys.txt ${keys_uniq} 
fi

# Composes all processed texts to one file for pulp's db
for i in ${final_data}full/*; do
    echo ${i} $(cat ${i}) >> texts_${stem}_${min_len}.txt
done

# Arranges topics by their popularity between all data.
# 'topics_summary_nums.txt' may be used in pulp for assigning spesific colors
# to most prominent topics.
python scripts/top_topics.py ${topics_sect}composition.txt \
    ${topics_sect}topics_summary_${stem} ${topics}
# --> ${topics_sect}topics_summary_nonstem.txt
# --> ${topics_sect}topics_summary_nonstem_plot.png
# --> ${topics_sect}topics_summary_nonstem_nums.txt

