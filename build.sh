#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

docker build -t validator:latest .
docker run --restart=always -d -p 8080:8080 validator
