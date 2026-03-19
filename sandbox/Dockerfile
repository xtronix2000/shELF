FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        strace \
    && rm -rf /var/lib/apt/lists/*

COPY tracer.sh /opt/tracer.sh
RUN chmod +x /opt/tracer.sh

CMD ["/opt/tracer.sh"]