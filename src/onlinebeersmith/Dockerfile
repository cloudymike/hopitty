FROM ubuntu:22.04
WORKDIR /hopitty

ENV AWS_ACCESS_KEY_ID='DUMMYIDEXAMPLE'
ENV AWS_SECRET_ACCESS_KEY='DUMMYEXAMPLEKEY'
ENV REGION='us-west-2'

RUN apt update
RUN apt install -y build-essential
RUN apt install -y curl
RUN apt install -y jq
RUN apt install -y wget

RUN apt install -y python3
RUN apt update
RUN apt install -y python3-pip

COPY ../../requirements.txt /requirements.txt
RUN /usr/bin/pip3 install -r /requirements.txt

COPY . .

RUN cd /hopitty/phidget/PhidgetsPython && python3 setup.py install

CMD ["/hopitty/src/onlinebeersmith/online2dynamo.sh"]

