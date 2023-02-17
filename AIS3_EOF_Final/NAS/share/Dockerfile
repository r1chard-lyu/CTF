FROM ubuntu:20.04
MAINTAINER u1f383

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy libseccomp-dev xinetd

RUN useradd -m nas
RUN chown -R root:root /home/nas
RUN chmod -R 755 /home/nas

CMD ["/usr/sbin/xinetd", "-dontfork"]