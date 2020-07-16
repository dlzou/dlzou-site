FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY /app /app/
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload
