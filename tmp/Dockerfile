
FROM ubuntu:14.04
MAINTAINER padro@cs.upc.edu

RUN apt-get update -q && \
    apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    apt-get install -y build-essential automake autoconf libtool wget \
                       libicu52 libboost-regex1.54.0 \
                       libboost-system1.54.0 libboost-program-options1.54.0 \
                       libboost-thread1.54.0 && \
    apt-get install -y libicu-dev libboost-regex-dev libboost-system-dev \
                       libboost-program-options-dev libboost-thread-dev \
                       zlib1g-dev &&\
    cd /root && \
    wget --progress=dot:giga https://github.com/TALP-UPC/FreeLing/releases/download/4.0/FreeLing-4.0.tar.gz && \
    tar xvzf FreeLing-4.0.tar.gz && \
    rm -rf FreeLing-4.0.tar.gz && \
    cd /root/FreeLing-4.0 && \
    autoreconf --install && \
    ./configure && \
    make -j4 && \
    make install

WORKDIR /root

