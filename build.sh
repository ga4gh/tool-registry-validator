#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

docker build -t validator:latest .
docker run -d -p 5000:5000 validator
