#!/bin/bash

BASE_DIR=~/SSL-IoT
CERTS=("Broker" "Subscriber" "Publisher")

for CERT in "${CERTS[@]}"; do
    
    if [[ "${CERT}" == "Broker" ]]; then
        DIR="${BASE_DIR}/Broker/config/certs/"
        sudo chown -R $USER:$USER "${DIR}"
    else
        DIR="${BASE_DIR}/${CERT}/certs/"
    fi

    # echo "${DIR}/*"
    rm ${DIR}*.crt
    rm ${DIR}*.key
    rm ${DIR}*.csr


done