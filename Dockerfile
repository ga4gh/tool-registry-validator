FROM ubuntu:latest
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN python setup.py install
RUN pip install -r validator/requirements.txt
ENTRYPOINT ["python"]
CMD ["validator/validator.py"]
