# We use devel because plugins_sagemaker-training needs gcc to build
# TODO get rid of plugins_sagemaker-training
FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source https://github.com/nebulaclouds/nebulasnacks

WORKDIR /root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Install basics
RUN apt-get update && apt-get install -y make build-essential libssl-dev curl

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip install awscli

WORKDIR /opt
RUN curl https://sdk.cloud.google.com > install.sh
RUN bash /opt/install.sh --install-dir=/opt
ENV PATH $PATH:/opt/google-cloud-sdk/bin
WORKDIR /root

# Install gcc , g++ and make
RUN apt-get update && apt-get install --no-install-recommends -y gcc g++
RUN echo 'installing make' \
    && apt-get install make

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /root/.
RUN pip install -r /root/requirements.txt

# Setup Sagemaker entrypoints
ENV SAGEMAKER_PROGRAM /opt/venv/bin/nebulakit_sagemaker_runner.py

# Copy the actual code
COPY . /root/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV NEBULA_INTERNAL_IMAGE $tag
