# Truthy
FROM ubuntu:14.04 

# Install dependency packages
RUN \
    apt-get update && \
    apt-get install -y git wget vim && \
    apt-get install -y python python-pip && \
    apt-get install -y python-numpy python-matplotlib python-termcolor python-scipy python-pyaudio

# Working directory
RUN mkdir /app
WORKDIR /app
RUN \
    git clone https://github.com/itspoma/audio-fingerprint-identifying-python && \
    mkdir -p audio-fingerprint-identifying-python/mp3
COPY motorcycle.mp3 audio-fingerprint-identifying-python/mp3

# Install pydub with source codes
COPY pydub-0.25.1.tar.gz .
# RUN \
#    tar xf pydub-0.25.1.tar.gz && \
#    python pydub-0.25.1v/setup.py install
