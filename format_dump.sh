#!/bin/bash

i=0
while IFS=$'\n' read -r line; do
    if [ $((i%2)) -eq 0 ];
    then
        echo $line | jq -c '{index: {_id: .index._id}}'
    else
        echo $line | jq -c '{title, page_id, text}'
    fi
    ((++i))
done
