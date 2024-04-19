#!/bin/bash

# fail if any command fails.
set -euo pipefail
# write all output to log file
log_file=ingest.log
exec 3>&1 1>"$log_file" 2>&1

date=20240415
wiki_url=https://dumps.wikimedia.org/other/cirrussearch/${date}/enwikiquote-${date}-cirrussearch-content.json.gz
raw_dump_file=wikiquote_raw.json.gz
elastic_url=https://localhost:9200
index_url="${elastic_url}/wikiquote"
success_file=success_$date

echo "Starting ingest process for date: $date" >&3


# exit if this script has already run successfully. 
if [ -e $success_file ]; then
    echo "Successfully ingested data for dump date: $date" >&3
    exit
fi 


# download the elasticsearch dump file from wikimedia.
if [ -e $raw_dump_file ]; then
    echo 'Skipping wikiquote dump download, file already exists.' >&3
else 
    echo 'Downloading wikiquote dump file.' >&3
    wget -nv $wiki_url -O $raw_dump_file
    # if wget did not return 200 then bail
    if [ $? -ne 0 ]; then
        echo "Failed to download dump file, see $log_file" >&3
        # clean up empty file that wget wrote.
        rm $raw_dump_file
        exit 1
    fi
fi


# split the large dump file into many smaller files.
# during the split pipe each line through our custom formatter which removes data we won't be using. 
chunk_count=0
if [ -d chunks ]; then
    chunk_count=$(ls chunks -1q | wc -l)
    echo 'Skipping dump file chunking, directory exists.' >&3
else 
    echo 'Splitting dump file into smaller chunks.' >&3
    mkdir -p chunks
    gunzip -c $raw_dump_file | split -d --filter='python3 format_bulk_data.py > $FILE' -l 500 - ./chunks/wikiquote_chunk_
    chunk_count=$(ls chunks -1q | wc -l)
    echo "Split file into $chunk_count chunk(s)." >&3
fi


# create the elastic index we will load the data into
exists_status_code=$(
    curl --silent --insecure -u elastic:elastic \
        -o /dev/null -w "%{http_code}" \
        -I "${index_url}?pretty"
)
if [ $exists_status_code = "200" ]; then
    echo 'Skipping index creation, index already exists.' >&3
else 
    echo 'Creating elasticsearch index.' >&3
    curl --insecure -u elastic:elastic \
        --silent -XPUT "$index_url" \
        -H "Content-Type: application/json" \
        -d @index_settings.json
    # fail if could not create index
    if [ $? -ne 0 ]; then
        echo "Failed to create elasticsearch index, see $log_file" >&3
        exit 1
    fi
fi


# use the bulk api to load each chunk into elastic
echo -en "Loading chunk(s) into elasticsearch" >&3
i=1
for file_name in chunks/*; do
    echo -en "\rLoading chunk(s) into elasticsearch: ${i}/${chunk_count}" >&3
    curl --silent --show-error --fail-with-body -w '\n' \
        --insecure -u elastic:elastic \
        -H "Content-Type: application/x-ndjson" \
        -XPOST "$index_url/_bulk" \
        --data-binary @"${file_name}" >> $log_file
    i=$((i + 1))
done
# flush to ensure all elastic writes all data to index
echo -e '\nFlushing elasticsearch index.' >&3
curl --fail-with-body --silent --insecure -u elastic:elastic \
    -X POST "$index_url/_flush?pretty"


# remove the chunks and original dump now that they've been loaded into elastic
echo 'Removing wikiquote dump and chunk files.' >&3
rm -r chunks
rm $raw_dump_file


# create the success file so this script will not be re-run on restarts
touch $success_file
echo "Ingest complete for date: $date" >&3
