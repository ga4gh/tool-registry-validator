FROM ubuntu:latest
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt-get update -y
# install node.js and npm
RUN apt-get -qq update && apt-get install -y wget nodejs && apt-get install -y npm && ln -s /usr/bin/nodejs /usr/bin/node
# install git
RUN apt-get install git -y
# install dredd 
RUN npm install -g dredd
# test versions 
RUN node -v && \
    npm -v && \
    dredd --version
RUN apt-get install -y python-pip python-dev build-essential
RUN git clone https://github.com/ga4gh/tool-registry-validator.git
WORKDIR tool-registry-validator
RUN git checkout feature/flask
RUN python setup.py install
RUN pip install -r validator/requirements.txt
RUN wget https://raw.githubusercontent.com/ga4gh/tool-registry-schemas/feature/trsv_changes/src/main/resources/swagger/ga4gh-tool-discovery.yaml -P validator
RUN python validator/createProcessedYAML.py
RUN python validator/createRelaxedYAML.py
ENTRYPOINT ["python"]
CMD ["validator/validator.py"]
