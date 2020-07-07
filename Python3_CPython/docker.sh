#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
IMAGE_TAG=anylang-rl-python3_cpython

docker build -t ${IMAGE_TAG} .
docker run \
    --rm \
    --mount type=bind,src=${SCRIPT_DIR}/../,dst=/anylang-rl \
    -w /anylang-rl/Python3_CPython \
    ${IMAGE_TAG} \
    ${@}
