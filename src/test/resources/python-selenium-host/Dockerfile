FROM ubuntu:18.04
LABEL maintainer="vlussenburg@xebialabs.com"

RUN apt-get -qq update -y && apt-get -qq install -y --no-install-recommends supervisor openssh-server python python-pip && pip install selenium && rm -rf /var/lib/apt/lists/*

COPY sshd_config /etc/ssh/sshd_config
RUN chmod 644 /etc/ssh/sshd_config && echo "root:xebialabs" | chpasswd
RUN mkdir -p /var/log/supervisor /var/run/sshd
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 22

CMD ["/usr/bin/supervisord"]