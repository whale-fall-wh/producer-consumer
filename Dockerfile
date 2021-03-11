FROM python:3.8.8-alpine

ARG CHANGE_SOURCE=true
RUN if [ ${CHANGE_SOURCE} = true ]; then \
  # 切换阿里云镜像
  sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/' /etc/apk/repositories \
;fi

COPY . /app

WORKDIR /app

RUN apk --no-cache add gcc libc-dev libxml2-dev libxslt-dev

RUN pip install -r requirements.txt