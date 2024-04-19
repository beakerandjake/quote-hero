#!/bin/bash

# fail if any command fails.
set -euo pipefail
# write all output to log file
log_file=ingest.log
exec 3>&1 1>"$log_file" 2>&1

date=20240415
url=https://dumps.wikimedia.org/other/cirrussearch/${date}/enwikiquote-${date}-cirrussearch-content.json.gz
raw_file=wikiquote_raw.json.gz


# download the elasticsearch dump file from wikimedia.
if [ -e $raw_file ]; then
    echo 'Skipping wikiquote dump download, file already exists.' >&3
else 
    echo 'Downloading wikiquote dump file.' >&3
    wget $url -O $raw_file
    # if wget did not return 200 then bail
    if [ $? -ne 0 ]; then
        echo "Failed to download dump file, see $log_file" >&3
        # clean up empty file that wget wrote.
        rm $raw_file
        exit 1
    fi
fi


# split the large dump file into many smaller files.
# during the split pipe each line through our custom formatter which removes data we won't be using. 
chunk_count=0
if [ -d chunks ]; then
    chunk_count=$(ls chunks -1q | wc -l)
    echo 'Not splitting dump file, chunk directory exists.' >&3
else 
    echo 'Splitting dump file into smaller chunks.' >&3
    mkdir -p chunks
    gunzip -c $raw_file | split -d --filter='python3 format_bulk_data.py > $FILE' -l 500 - ./chunks/wikiquote_chunk_
    chunk_count=$(ls chunks -1q | wc -l)
    echo "Split file into $chunk_count chunk(s)." >&3
fi

# create the elastic index we will load the data into
echo 'Creating elasticsearch index.' >&3
curl --fail-with-body --silent --show-error -w '\n' --insecure -u elastic:elastic \
    -XPUT "https://localhost:9200/wikiquote" \
    -H "Content-Type: application/json" \
    -d @index_settings.json
# fail if could not create index
if [ $? -ne 0 ]; then
    echo "Failed to create elasticsearch index, see $log_file" >&3
    exit 1
fi


# use the bulk api to load each chunk into elastic
echo -en "Loading chunk(s) into elasticsearch" >&3
i=1
for file_name in chunks/*; do
    echo -en "\rLoading chunk(s) into elasticsearch: ${i}/${chunk_count}" >&3
    curl --silent --show-error --fail-with-body -w '\n' \
        --insecure -u elastic:elastic \
        -H "Content-Type: application/x-ndjson" \
        -XPOST 'https://localhost:9200/wikiquote/_bulk' \
        --data-binary @"${file_name}" >> ingest.log
    i=$((i + 1))
done
# flush to ensure all elastic writes all data to index
echo -e '\nFlushing elasticsearch index.' >&3
curl --fail-with-body --silent --insecure -u elastic:elastic \
    -X POST "https://localhost:9200/wikiquote/_flush?pretty"


# remove the chunks and original dump now that they've been loaded into elastic
echo 'Removing wikimedia dump and chunk files.' >&3
rm -r chunks
rm $raw_file


echo 'Ingest complete.' >&3
