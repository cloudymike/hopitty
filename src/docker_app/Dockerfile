# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

#ENV REDIS_SERVER='redis'
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add libffi-dev
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
#COPY config.py config.py
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["flask", "run"]