FROM debian:12-slim

RUN apt-get update \
    && apt-get install -y build-essential strace \
    && rm -rf /var/lib/apt/lists/*

COPY script.sh /opt/script.sh

RUN chmod +x /opt/script.sh

WORKDIR /src

CMD ["/opt/script.sh"]
