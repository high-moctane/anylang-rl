FROM buildpack-deps:latest

ENV HOME=/root

RUN apt-get update

RUN apt-get install -y time

# Go
ENV GO_VERSION=1.14.4
ENV PATH=$PATH:/usr/local/go/bin
RUN wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz
RUN rm go$GO_VERSION.linux-amd64.tar.gz

CMD ["/bin/bash"]