# pull official base image
FROM python:3.12

# set working directory
WORKDIR /api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml /api

# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc vim git curl openssh-server \
  && apt-get clean

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test

RUN  echo 'test:test' | chpasswd

RUN service ssh start
RUN /usr/sbin/sshd

RUN mkdir /api/uploads
RUN chmod 777 /api/uploads

EXPOSE 22

RUN python -m pip install --upgrade pip
RUN pip install trio
RUN pip install python-dotenv

RUN pip install pinecone-client
RUN pip install langchain-community

RUN pip install -U -q google-generativeai
RUN pip install langchain-google-genai

RUN pip install -qU openai
RUN pip install -qU langchain-openai

RUN pip install -qU streamlit
RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
RUN poetry lock && poetry install

