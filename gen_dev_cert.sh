#!/bin/bash

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <last-octet-of-ip>"
    exit 1
fi

IP="192.168.1.$1"
DAYS=$((5 * 365)) # 5 years

# Updated configuration block
CONFIG="
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = SomeState
L = SomeCity
O = SomeOrganization
OU = SomeOrganizationalUnit
CN = $IP

[v3_req]
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP
"

# Generate private key and certificate
openssl req -x509 -nodes -days $DAYS -newkey rsa:2048 -keyout "$IP.key" -out "$IP.crt" -config <(echo "$CONFIG")

echo "Certificate and private key generated for IP $IP"
