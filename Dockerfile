FROM python:3.9-buster

WORKDIR /var/socli

COPY . .

RUN python setup.py install

CMD /usr/local/bin/socli
