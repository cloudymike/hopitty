FROM ubuntu:22.04
WORKDIR /hopitty

ENV AWS_ACCESS_KEY_ID='DUMMYIDEXAMPLE'
ENV AWS_SECRET_ACCESS_KEY='DUMMYEXAMPLEKEY'
ENV REGION='us-west-2'

#RUN apk add --no-cache gcc musl-dev linux-headers
#RUN apt install --no-cache gcc 
#RUN apt install --no-cache glibc-dev
#RUN apt install --no-cache linux-headers
#RUN apt install  libffi-dev
#RUN apt install  bash

RUN apt update
RUN apt install -y build-essential
RUN apt install -y curl
RUN apt install -y jq
RUN apt install -y wget
RUN apt install -y python2
RUN apt update
RUN apt install -y python-pip

COPY ../../requirements.txt /requirements.txt
RUN /usr/bin/pip2 install -r /requirements.txt

COPY . .

#RUN cd phidget/PhidgetsPython
RUN cd /hopitty/phidget/PhidgetsPython && python2 setup.py install
#RUN cd /hopitty

RUN apt install -y python3
RUN apt install -y python3-pip
RUN python3 -m pip install -r onlinebeersmith/requirements.txt


CMD ["sleep", "infinity"]