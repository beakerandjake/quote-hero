#!/bin/bash

date=20240415
url=https://dumps.wikimedia.org/other/cirrussearch/${date}/enwikiquote-${date}-cirrussearch-content.json.gz
raw_file=wikiquote.json.gz

# download the dump from wikimedia.org
# echo "downloading dump file"
# wget $url -O $raw_file

# split the large dump file into many smaller files.
# during the split pipe each line through our custom formatter which removes data we won't be using. 
echo 'splitting dump file into smaller chunks'
mkdir -p chunks
gunzip -c $raw_file | split -d --filter='python3 format_input.py > $FILE' -l 500 - ./chunks/wikiquote_chunk_

# 
