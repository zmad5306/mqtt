FROM python:3.13-slim

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "consumer.py" ]
