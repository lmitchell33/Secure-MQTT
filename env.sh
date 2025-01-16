#!/bin/bash

# NOTE: This must be ran with source env.sh to run in the current shell

while IFS= read -r line; do
    # Ignore lines that are empty or start with a comment
    if [[ ! -z "$line" && ! "$line" =~ ^# ]]; then
        echo "${line}"
        export "$line"
    fi
done < .env