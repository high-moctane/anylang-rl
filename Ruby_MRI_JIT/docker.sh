#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
IMAGE_TAG=anylang-rl-ruby_mri_jit

docker build -t ${IMAGE_TAG} .
docker run \
    --rm \
    -it \
    --mount type=bind,src=${SCRIPT_DIR}/../,dst=/anylang-rl \
    -w /anylang-rl/Ruby_MRI_JIT \
    ${IMAGE_TAG} \
    ${@}
