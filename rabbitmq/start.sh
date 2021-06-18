#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

export RABBITMQ_CONFIG_FILE="$(pwd)/__rabbitmq.conf"
export RABBITMQ_LOG_BASE="$(pwd)/logs/"
export RABBITMQ_MNESIA_BASE="$(pwd)/db/"
export RABBITMQ_PID_FILE="$(pwd)/db/.pid"
export RABBITMQ_CONSOLE_LOG="new"
export RABBITMQ_LOGS="$(pwd)/logs/rabbitmq.log"

CROOT="$(pwd)/certs"

sed -e "s#^.*ssl_options.cacertfile.*\$#ssl_options.cacertfile=${CROOT}/rootCA.crt#g" \
	-e "s#^.*ssl_options.certfile.*\$#ssl_options.certfile=${CROOT}/server.crt#g" \
	-e "s#^.*ssl_options.keyfile.*\$#ssl_options.keyfile=${CROOT}/server.key#g" \
	"$(pwd)/rabbitmq.conf" >"$RABBITMQ_CONFIG_FILE"

mkdir -p "$RABBITMQ_LOG_BASE" "$RABBITMQ_MNESIA_BASE"
chown rabbitmq "$RABBITMQ_LOG_BASE" "$RABBITMQ_MNESIA_BASE" -R
rabbitmq-server

# rabbitmqctl add_user xxxx yyyy
# rabbitmqctl set_permissions xxxx ".*" ".*" ".*"
# rabbitmq-plugins enable rabbitmq_management
