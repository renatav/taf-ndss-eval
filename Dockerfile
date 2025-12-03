FROM ubuntu:24.04

RUN apt update && apt install python3 python3.12-venv python3-pip build-essential git -y

WORKDIR /root

RUN pip install --break-system-packages taf==0.36.0

RUN git config --global user.name "Your Name"
RUN git config --global user.email "your.email@example.com"

RUN echo "alias python=python3" >> ~/.bashrc

ADD . .
