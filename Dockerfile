FROM python:alpine3.6

RUN pip install --upgrade pip
RUN mkdir /src
WORKDIR /src

COPY . .
