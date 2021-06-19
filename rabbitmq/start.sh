#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

export RABBITMQ_CONFIG_FILE="$(pwd)/__rabbitmq.conf"
export RABBITMQ_LOG_BASE="$(pwd)/logs/"
export RABBITMQ_MNESIA_BASE="$(pwd)/db/"
export RABBITMQ_PID_FILE="$(pwd)/db/.pid"
export RABBITMQ_CONSOLE_LOG="new"
export RABBITMQ_LOGS="$(pwd)/logs/rabbitmq.log"

PROJECT_PATH="$(realpath -m ..)"
CROOT="$(pwd)/certs"

sed -e "s#^.*ssl_options.cacertfile.*\$#ssl_options.cacertfile=${CROOT}/rootCA.crt#g" \
	-e "s#^.*ssl_options.certfile.*\$#ssl_options.certfile=${CROOT}/server.crt#g" \
	-e "s#^.*ssl_options.keyfile.*\$#ssl_options.keyfile=${CROOT}/server.key#g" \
	"$(pwd)/rabbitmq.conf" >"$RABBITMQ_CONFIG_FILE"

if [[ -f "$PROJECT_PATH/.env" ]]; then
	source "$PROJECT_PATH/.env"
fi

RMQ_USER=test-username
RMQ_PASS=test-password

SRV_NAME=test-rabbitmq.service
if systemctl is-failed --quiet "$SRV_NAME"; then
	systemctl reset-failed "$SRV_NAME"
fi
if ! systemctl is-active --quiet "$SRV_NAME"; then
	rm -rf "$RABBITMQ_LOG_BASE"
	mkdir -p "$RABBITMQ_LOG_BASE" "$RABBITMQ_MNESIA_BASE"
	chown rabbitmq "$RABBITMQ_LOG_BASE" "$RABBITMQ_MNESIA_BASE" -R

	systemd-run --same-dir --no-ask-password --unit="$SRV_NAME" --quiet \
		"--setenv=HOSTNAME=$HOSTNAME" \
		"--setenv=RABBITMQ_CONFIG_FILE=$RABBITMQ_CONFIG_FILE" \
		"--setenv=RABBITMQ_LOG_BASE=$RABBITMQ_LOG_BASE" \
		"--setenv=RABBITMQ_MNESIA_BASE=$RABBITMQ_MNESIA_BASE" \
		"--setenv=RABBITMQ_PID_FILE=$RABBITMQ_PID_FILE" \
		"--setenv=RABBITMQ_CONSOLE_LOG=$RABBITMQ_CONSOLE_LOG" \
		"--setenv=RABBITMQ_LOGS=$RABBITMQ_LOGS" \
		rabbitmq-server
fi

while ! grep --fixed-strings 'started TLS (SSL) listener on' "$RABBITMQ_LOGS" 2>/dev/null; do
	sleep 5
done

rabbitmqctl add_user "$RMQ_USER" "$RMQ_PASS" || rabbitmqctl change_password "$RMQ_USER" "$RMQ_PASS"
rabbitmqctl set_permissions "$RMQ_USER" ".*" ".*" ".*"
rabbitmq-plugins enable rabbitmq_management

echo "RabbitMQ已启动"
