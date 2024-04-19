#!/bin/bash

dump=wikiquote.json

echo 'splitting data into chunks'

mkdir -p chunks
split -a 10  -l 500 $dump ./chunks/wikiquote_chunk_

# todo: --filter='python3 format_input.py'
# for file in ./chunks/*
# do
#     cat $file | 
# done
