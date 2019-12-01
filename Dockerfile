FROM python:alpine3.6

RUN pip install --upgrade pip
RUN apk add --no-cache build-base linux-headers libffi-dev gcc musl-dev python3-dev libressl-dev
RUN mkdir /src
WORKDIR /src

COPY . .
RUN pip install oci
RUN pip install -e .

ENTRYPOINT [ "ociman" ]

