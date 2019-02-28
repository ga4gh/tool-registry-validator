FROM ubuntu:18.04
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt-get update -y
# install node.js and npm
RUN apt-get -qq update
RUN apt-get install curl -y
RUN apt-get install -y gnupg2
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs
# install git
RUN apt-get install git -y
# install dredd
RUN npm install -g dredd@8.0.3 --unsafe-perm
# test versions
RUN node -v && \
    npm -v && \
    dredd --version
RUN apt-get install -y python-pip python-dev build-essential
# This apparently forces --no-cache for git cloning and sadly everything after it
# TODO: Change all feature/flask in this file to the correct branch
ADD https://api.github.com/repos/ga4gh/tool-registry-validator/compare/feature/validatorUpdate...HEAD /dev/null
RUN git clone https://github.com/ga4gh/tool-registry-validator.git

WORKDIR tool-registry-validator
RUN git checkout feature/validatorUpdate
RUN python setup.py install
RUN pip install -r validator/requirements.txt
RUN pip install uwsgi -I --no-cache-dir
WORKDIR validator
ENTRYPOINT ["uwsgi", "--http-socket", ":8080", "--wsgi-file", "validator.py", "--callable", "app", "--enable-threads", "--thunder-lock", "-p", "1"]