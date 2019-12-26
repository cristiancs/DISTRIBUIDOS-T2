FROM       python:3.7.4-alpine3.9

WORKDIR    /app
ENV PYTHONUNBUFFERED 1
COPY requirements.txt ./
RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update alpine-sdk make gcc python3-dev python-dev libxslt-dev libxml2-dev libc-dev openssl-dev libffi-dev zlib-dev py-pip openssh \
    && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt


CMD        ["python", "./server.py"]