#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
IMAGE_TAG=anylang-rl-rust_rustc

docker build -t ${IMAGE_TAG} .
docker run \
    --rm \
    --mount type=bind,src=${SCRIPT_DIR}/../,dst=/anylang-rl \
    -w /anylang-rl/Rust_rustc \
    ${IMAGE_TAG} \
    ${@}
