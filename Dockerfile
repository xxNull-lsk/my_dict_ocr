FROM ubuntu:20.04

ADD . /app
WORKDIR /app/src
ENTRYPOINT ["python3", "main.py"]
EXPOSE 12126

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip libglib2.0-dev libsm6 libxext6 libxrender-dev && \
    mkdir -p /root/.pip && \
    cp /app/cfg/pip.conf /root/.pip/pip.conf && \
    pip3 install -r /app/requirements.txt && \
    rm -rf /app/test && \
    rm -rf /app/.git && \
    rm -rf /app/cfg && \
    rm -rf /root/.cache && \
    rm -rf /var/lib/apt/lists && \
    echo "Asia/Shanghai" > /etc/timezone && \
    rm -rf /etc/localtime && \
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
