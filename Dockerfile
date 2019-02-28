FROM node:10.15.2-slim
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt-get update -yq
# install git
RUN apt-get install git -yq
# install dredd
RUN npm install -g dredd@8.0.3 --unsafe-perm --allow-root
# install python
RUN apt-get install python-pip python-dev build-essential -yq
# This apparently forces --no-cache for git cloning and sadly everything after it
# TODO: Change all feature/flask in this file to the correct branch
ADD https://api.github.com/repos/ga4gh/tool-registry-validator/compare/feature/README...HEAD /dev/null
RUN git clone https://github.com/ga4gh/tool-registry-validator.git

WORKDIR tool-registry-validator
RUN git checkout feature/README
RUN pip install -r validator/requirements.txt
RUN pip install uwsgi -I --no-cache-dir
WORKDIR validator
ENTRYPOINT ["uwsgi", "--http-socket", ":8080", "--wsgi-file", "validator.py", "--callable", "app", "--enable-threads", "--thunder-lock", "-p", "1"]
