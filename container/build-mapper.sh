#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath -m "${BASH_SOURCE[0]}")")"
source "./builder/functions-build.sh"
arg_finish

declare -r CACHE="blivedm-record-mapper"

#########
STEP="安装python并编译依赖"
make_base_image_by_fedora_pip "${CACHE}" "../src/mapper/requirements.txt" "scripts/build-deps.lst" "scripts/runtime-deps-mapper.lst"
#########

#########
STEP="复制代码"
FILES=("mapper" "mylib" "mapper.py" "entrypoint.sh")
pushd .. &>/dev/null
function hash_files() {
	for I in "${FILES[@]}"; do
		hash_path "src/$I"
	done
}
function copy_files() {
	for I in "${FILES[@]}"; do
		buildah add "$1" "src/$I" "/app/$I"
	done
}
buildah_cache2 "$CACHE" hash_files copy_files
popd &>/dev/null
#########

STEP="配置镜像信息"
buildah_config "$CACHE" --stop-signal=SIGINT --entrypoint '["/bin/bash","/app/entrypoint.sh"]' \
	"--env=APP=mapper" \
	--author "GongT <admin@gongt.me>" --created-by "#MAGIC!" --label name=gongt/certbot-dns
info "settings updated..."

RESULT=$(create_if_not "certbot" "$BUILDAH_LAST_IMAGE")
buildah commit "$RESULT" docker.io/gongt/bilibili-live-danmu-mapper
info "Done!"
