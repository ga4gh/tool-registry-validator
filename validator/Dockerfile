FROM ubuntu:latest
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN ls
RUN python ../setup.py install
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["validator.py"]
