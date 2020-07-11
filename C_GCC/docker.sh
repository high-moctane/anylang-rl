#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
IMAGE_TAG=anylang-rl-c_gcc

docker build -t ${IMAGE_TAG} .
docker run \
    --rm \
    -it \
    --mount type=bind,src=${SCRIPT_DIR}/../,dst=/anylang-rl \
    -w /anylang-rl/C_GCC \
    ${IMAGE_TAG} \
    ${@}