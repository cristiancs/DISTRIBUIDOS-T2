FROM       python:3.7.4-alpine3.9

WORKDIR    /app
ENV PYTHONUNBUFFERED 1
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD        ["python", "./client.py"]