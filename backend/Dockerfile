FROM python:3.8
ENV PYTHONUNBUFFERED 1

ADD /app /app/
ADD requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt
