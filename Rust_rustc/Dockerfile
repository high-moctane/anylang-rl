FROM buildpack-deps:latest

ENV HOME=/root

RUN apt-get update
RUN apt-get install -y time

# _plotter
RUN apt-get -y install python3-pip
RUN pip3 install matplotlib=="3.2.2" numpy=="1.19.0" Pillow=="7.2.0"

# Rust
ENV PATH=$PATH:$HOME/.cargo/bin
ENV RUST_VERSION=1.44.1
ENV RUST_BACKTRACE=1
RUN wget -O rustup-init.sh http://sh.rustup.rs
RUN sh ./rustup-init.sh -y --default-toolchain $RUST_VERSION
RUN rm rustup-init.sh

CMD ["/bin/bash"]