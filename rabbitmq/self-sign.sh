#!/usr/bin/env bash

## https://docs.vmware.com/en/vCloud-Availability-for-vCloud-Director/2.0/com.vmware.vcavcd.install.config.doc/GUID-8C344104-47E5-46A3-95C7-B11845C6907A.html

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

mkdir -p certs
cd certs

if [[ -f rootca.jks ]]; then
	echo "cert already exists"
	exit 1
fi

function x() {
	echo -e " + \e[2m$*\e[0m"
	"$@"
}

if [[ ! -f rootCA.key ]]; then
	x openssl genrsa -out rootCA.key 4096
	x openssl req -x509 -subj "/C=CN/ST=SH/O=MyOrg/CN=example.com" -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt
fi

if [[ ! -f server.key ]]; then
	x openssl genrsa -out server.key 2048
fi

if [[ ! -f server.csr ]]; then
	x openssl req -new -sha256 -key server.key -subj "/C=CN/ST=SH/O=MyOrg/CN=example.com" -out server.csr
fi

if [[ ! -f server.crt ]]; then
	x openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server.crt -days 365 -sha256
fi

chown rabbitmq . -R
