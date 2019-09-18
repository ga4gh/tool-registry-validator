FROM node:12.10-slim
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt update -yq
# install git
RUN apt install git -yq
# install dredd
RUN npm install -g dredd@12.0.7 --unsafe-perm --allow-root
# install python
RUN apt install python-pip -yq
# set branch
ARG BRANCH=develop
# This apparently forces --no-cache for git cloning and sadly everything after it
ADD https://api.github.com/repos/ga4gh/tool-registry-validator/compare/${BRANCH}...HEAD /dev/null
RUN git clone https://github.com/ga4gh/tool-registry-validator.git

WORKDIR tool-registry-validator
RUN git checkout ${BRANCH}
RUN pip install -r validator/requirements.txt
RUN pip install uwsgi -I --no-cache-dir
WORKDIR validator
ENTRYPOINT ["uwsgi", "--http-socket", ":8080", "--wsgi-file", "validator.py", "--callable", "app", "--enable-threads", "--thunder-lock", "-p", "1"]
