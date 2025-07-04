#!/bin/bash

# create a private key
generate_key() {
    local key_path=$1
    openssl genrsa -out "${key_path}" 2048
}

# create a CSR
generate_csr() {
    local key_path=$1
    local csr_path=$2
    local subj=$3
    openssl req -new \
    -key "${key_path}" \
    -out "${csr_path}" \
    -subj "${subj}"
}

# Sign theCSR
sign_csr() {
    local csr_path=$1
    local cert_path=$2
    local ca_cert=$3
    local ca_key=$4
    local ext_file=$5

    openssl x509 -req \
        -in "${csr_path}" \
        -CA "${ca_cert}" \
        -CAkey "${ca_key}" \
        -CAcreateserial \
        -out "${cert_path}" \
        -sha256 \
        -days 365 \
        -extfile "${ext_file}"
}

# Base working directory
BASE_DIR=./../
CERTS=("Broker" "Subscriber" "Publisher")

# CA setup
CA_KEY="${BASE_DIR}/Broker/config/certs/ca.key"
CA_CERT="${BASE_DIR}/Broker/config/certs/ca.crt"
CA_CNF="${BASE_DIR}/Broker/config/certs/ca.cnf"


# create the CA certificate
generate_key "${CA_KEY}"
openssl req -x509 -new -nodes \
    -key "${CA_KEY}" \
    -sha256 \
    -days 365 \
    -out "${CA_CERT}" \
    -config "${CA_CNF}" \
    -extensions v3_ca \
    -addext "keyUsage = critical, Certificate Sign, CRL Sign"

if [[ ! -f "${CA_CERT}" ]]; then
    echo "CA certificate not found"
    exit 1
fi

BROKER_EXT="${BASE_DIR}/Broker/config/certs/ca.ext"

# Generate Certificates and keys for the Broker, Subscriber, and Publisher
for CERT in "${CERTS[@]}"; do

    if [[ "${CERT}" == "Broker" ]]; then
        DIR="${BASE_DIR}/Broker/config/certs"
    else
        DIR="${BASE_DIR}/${CERT}/certs"
    fi

    CURR_KEY="${DIR}/${CERT,,}.key"
    CURR_CSR="${DIR}/${CERT,,}.csr"
    CERT_PATH="${DIR}/${CERT,,}.crt"

    # generate the keys and certificates
    generate_key "${CURR_KEY}"
    generate_csr "${CURR_KEY}" "${CURR_CSR}" "/C=US/ST=Pennsylvania/L=Pittsburgh/O=Duquesne/OU=CS/CN=${CERT}"
    sign_csr "${CURR_CSR}" "${CERT_PATH}" "${CA_CERT}" "${CA_KEY}" "${BROKER_EXT}"
done


# Verify 
echo "Verifying certificates..."
for CERT in "${CERTS[@]}"; do
    
    if [[ "${CERT}" == "Broker" ]]; then
        DIR="${BASE_DIR}/Broker/config/certs"
    else
        DIR="${BASE_DIR}/${CERT}/certs"
    fi

    CERT_PATH="${DIR}/${CERT,,}.crt"

    if [[ -f "${CERT_PATH}" ]]; then
        openssl verify -CAfile "${CA_CERT}" "${CERT_PATH}"
        if [[ $? -eq 0 ]]; then
            echo "${CERT} certificate verified successfully"
        else
            echo "Verification failed for ${CERT} certificate"
        fi
    else
        echo "${CERT} certificate not found at ${CERT_PATH}"
    fi
done

echo "Verification complete"