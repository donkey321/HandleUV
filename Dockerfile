FROM python:alpine3.10

WORKDIR /HandleUV

COPY . /HandleUV
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories 
# 安装gcc，如果有包需要则安装
RUN apk add build-base
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

RUN pip install -U pip
RUN pip install -r requirements.txt
EXPOSE 9595
CMD python manage.py runserver 0.0.0.0:9595
