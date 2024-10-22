# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add libffi-dev
RUN apk add bash
RUN apk add curl
RUN apk add jq
RUN pip install --upgrade pip
COPY . .
#RUN pip install -r onlinebeersmith/requirements.txt
CMD ["sleep", "infinity"]