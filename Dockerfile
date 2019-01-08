FROM python:3.7.1-alpine3.7

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# get our basic-needs sorted
RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN apk update

RUN mkdir -p /opt /app

ADD . /app
WORKDIR /app
RUN pip install -e .
ENTRYPOINT ["slack-machine"]