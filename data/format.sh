#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

for F in *.json5; do
	F=$(basename "$F" .json5)
	echo "$F"
	while IFS=$'\n' read -r LINE; do
		[[ $LINE ]] || continue
		[[ $LINE != //* ]] || continue
		echo "$LINE" | sed 's/: None\b/: null/g' | json5
		echo ""
	done <"$F.json5" | jq -s >"$F.json"
done
