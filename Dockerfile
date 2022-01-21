FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /itechart
COPY requirements.txt /itechart
RUN pip install -r requirements.txt
COPY ./ /itechart