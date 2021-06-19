#!/usr/bin/env bash

set -Eeuo pipefail
cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

podman rm blivedm-rec-localtest &>/dev/null || true

if [[ $* == "-d" ]]; then
	IO_ARG=(-d -t)
else
	IO_ARG=(--rm -it)
fi

IO_ARG+=("--volume=$(pwd):/__src:ro" "--network=host")

source .env
ARGS=(
	"--server=test-username:test-password@10.0.0.102:5671"
	"--cacert=/__src/rabbitmq/certs/server.crt"
	"--filter=/__src/src/collector/filter.example.py"
	"1485080"  # 撒子
	"21712635" # 狮子
	"22333522" # 万子
	"21627536" # 嘻嘻
	"21919321" # 猫猫
	"505645"   # 我
	"23178720" # 我老婆
)

set -x
podman run --name blivedm-rec-localtest "${IO_ARG[@]}" docker.io/gongt/bilibili-live-dnamu-recorder "${ARGS[@]}"
