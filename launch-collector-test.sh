#!/usr/bin/env bash

set -Eeuo pipefail
cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

podman rm blivedm-rec-localtest &>/dev/null || true

if [[ $* == "-d" ]]; then
	IO_ARG=(-d -t)
else
	IO_ARG=(--rm -it)
fi

IO_ARG+=(
	"--volume=$(pwd):/__src:ro"
	"--network=host"
)

ARGS=(
	"--server=test-username:test-password@127.0.0.1:5671"
	"--cacert=/__src/rabbitmq/certs/server.crt"
	"--filter=/__src/src/collector/filter.example.py"
	"5085"     # 依然小智
	"704808"   # 张京华
	"22816111" # 冬雪莲
	"1485080"  # 撒子
	"21919321" # 猫猫
	"21712635" # 狮子
	"22333522" # 万子
	"21627536" # 嘻嘻
	"505645"   # 我
	"23178720" # 我老婆
	"22839866" # 惠惠
	"23118640" # 昼暮Nyx
	"23053960" # 梨夏Erika
	"22233836" # 耗子
)

set -x
podman run --name blivedm-rec-localtest "${IO_ARG[@]}" docker.io/gongt/bilibili-live-danmu-collector "${ARGS[@]}"
