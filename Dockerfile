# pull the official base image
FROM python:3

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET 8#b29g)o!7f^g)w!aoigzxnesa3_vahpv)v^$u(@-%(vt57h*+
ENV API_TOKEN Tpk_059b97af715d417d9f49f50b51b1c448

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app
