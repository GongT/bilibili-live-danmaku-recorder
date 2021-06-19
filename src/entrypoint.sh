#!/bin/sh

set -eu

if [ "$*" = "sh" ]; then
	exec sh --login -i
fi

echo "running $APP $*" >&2
cd /app
python "${APP}.py" "$@"
