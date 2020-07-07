#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
IMAGE_TAG=anylang-rl-go_go

docker build -t ${IMAGE_TAG} .
docker run \
    --rm \
    -it \
    --mount type=bind,src=${SCRIPT_DIR}/../,dst=/anylang-rl \
    -w /anylang-rl/Go_go \
    ${IMAGE_TAG} \
    ${@}
