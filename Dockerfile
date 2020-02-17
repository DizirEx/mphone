FROM python:3.7

ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install socat python3-gpg -y 

RUN pip3 install -r requirements.txt
CMD socat TCP-LISTEN:3333,fork,reuseaddr EXEC:'python3 service.py',stderr

