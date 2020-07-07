FROM buildpack-deps:latest

ENV HOME=/root

RUN apt-get update

RUN apt-get install -y time

# _plotter
RUN apt-get -y install python3-pip
RUN pip3 install matplotlib=="3.2.2" numpy=="1.19.0" Pillow=="7.2.0"

# PyPy
ENV PYPY_VERSION=3.6-v7.3.1
ENV PATH=$PATH:/usr/local/pypy3/bin
RUN wget https://bitbucket.org/pypy/pypy/downloads/pypy${PYPY_VERSION}-linux64.tar.bz2
RUN tar -xf pypy${PYPY_VERSION}-linux64.tar.bz2
RUN mv pypy${PYPY_VERSION}-linux64 /usr/local/pypy3
RUN rm pypy${PYPY_VERSION}-linux64.tar.bz2

CMD ["/bin/bash"]
