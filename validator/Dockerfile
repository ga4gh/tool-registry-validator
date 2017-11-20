FROM ubuntu:latest
MAINTAINER Gary Luu "gary.luu@oicr.on.ca"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN ls
RUN python ../setup.py install
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["wget", "https://raw.githubusercontent.com/ga4gh/tool-registry-schemas/feature/trsv_changes/src/main/resources/swagger/ga4gh-tool-discovery.yaml"]
ENTRYPOINT ["python"]
CMD ["validator.py"]
