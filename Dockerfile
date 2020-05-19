FROM ubuntu:18.04 as ngspice_build

LABEL maintainer="Clément Vial <clement.vial {at} protonmail {dot} com >"

ENV NGSPICE_VERSION 32

# installs for building of ngspice
RUN apt update && apt install -y \
    autoconf \
    automake \
    bison \
    curl \
    flex \
    g++ \
    libx11-dev \
    # libxaw-dev \
    libtool \
    make \
    libreadline-dev \
    libncurses5-dev \
    libncursesw5-dev

# building ngspice
RUN curl -fSL https://github.com/imr/ngspice/archive/ngspice-$NGSPICE_VERSION.tar.gz -o ngspice.tar.gz \
    && mkdir -p /usr/src \
    && tar -zxC /usr/src -f ngspice.tar.gz \
    && rm ngspice.tar.gz \
    && cd /usr/src/ngspice-ngspice-$NGSPICE_VERSION \
    && ./autogen.sh \
    && ./configure --with-x --with-readline=yes --with-ngshared --disable-debug --enable-cider --enable-openmp --enable-xspice \
    && make 2>&1 | tee make.log && make install
    # && rm -rf  /usr/src/ngspice-ngspice-$NGSPICE_VERSION

# RUN apt install libx11 libxaw

ENV LD_LIBRARY_PATH /usr/local/lib

# install python3
RUN apt install -y software-properties-common wget && add-apt-repository ppa:deadsnakes/ppa -y && apt install -y python3 python3-pip

# install pyspice and lcapy
RUN pip3 install pyspice lcapy jupyterlab pandas

# Install lcapy
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
ENV DEBIAN_FRONTEND noninteractive
RUN apt install -y tzdata
RUN apt install -y texlive-latex-base texlive-pictures texlive-latex-extra imagemagick ghostscript libjs-mathjax fonts-mathjax

# set up jupyterlab
RUN jupyter-lab --generate-config && \
    sed -i "s/#c.NotebookApp.allow_origin = ''/c.NotebookApp.allow_origin = ''/g"  /root/.jupyter/jupyter_notebook_config.py && \
    sed -i "s/#c.NotebookApp.token = '<generated>'/c.NotebookApp.token = ''/g"  /root/.jupyter/jupyter_notebook_config.py

