#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

curl -O https://raw.githubusercontent.com/ga4gh/tool-registry-schemas/feature/trsv_changes/src/main/resources/swagger/ga4gh-tool-discovery.yaml
docker build -t validator:latest .
docker run -d -p 5000:5000 validator
