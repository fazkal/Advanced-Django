FROM python:3.12.3-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requiremets.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requiremets.txt

COPY ./core /app/

