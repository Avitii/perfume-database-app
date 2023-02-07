FROM python:3.11.1

LABEL Maintainer="81411-klimek"

WORKDIR /app
COPY . /app

RUN apt update && apt install libzbar0 -y
RUN pip install opencv-python-headless pyzbar rich

CMD python ./main.py