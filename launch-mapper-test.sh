#!/usr/bin/env bash

set -Eeuo pipefail
cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

podman rm blivedm-map-localtest &>/dev/null || true

if [[ $* == "-d" ]]; then
	IO_ARG=(-d -t)
else
	IO_ARG=(--rm -it)
fi

IO_ARG+=("--volume=$(pwd):/__src:ro" "--volume=/dev/shm/container-shared-socksets:/dev/shm/container-shared-socksets")

ARGS=(
	"--database=mariadb+mysqldb://blivedm-record:blivedm-record@localhost:3306/blivedm-record?unix_socket=/dev/shm/container-shared-socksets/mariadb.sock"
	"--server=test-username:test-password@10.0.0.102:5671"
	"--cacert=/__src/rabbitmq/certs/server.crt"
)

set -x
podman run --name blivedm-map-localtest "${IO_ARG[@]}" docker.io/gongt/bilibili-live-danmu-mapper "${ARGS[@]}"
