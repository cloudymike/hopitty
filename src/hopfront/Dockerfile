# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV FN_AUTH_REDIRECT_URI=http://localhost:8080/google/auth
ENV FN_BASE_URI=http://localhost:8080

ENV AWS_ACCESS_KEY_ID='DUMMYIDEXAMPLE'
ENV AWS_SECRET_ACCESS_KEY='DUMMYEXAMPLEKEY'
ENV REGION='us-west-2'

#ENV REDIS_SERVER='redis'
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add libffi-dev
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
#COPY config.py config.py
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
#CMD ["flask", "run"]
CMD ["python", "./web.py", "-H", "192.168.62.151", "-D", "http://dynamodb:8000"]
#CMD ["python", "./web.py", "-H", "192.168.62.151", "-D", "http://192.168.62.151:8000"]
