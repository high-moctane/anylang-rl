FROM buildpack-deps:latest

ENV HOME=/root

RUN apt-get update

# _plotter
RUN apt-get -y install python3-pip
RUN pip3 install matplotlib=="3.2.2" numpy=="1.19.0" Pillow=="7.2.0"

CMD ["/bin/bash"]