FROM ubuntu:23.04

COPY requirements.txt /
ADD . /app

RUN apt update
RUN apt install -y python3 python3-pip python3-venv
RUN apt install -y grokj2k-tools exiftool

RUN python3 -m venv /venv
RUN . /venv/bin/activate && pip install -r /requirements.txt

EXPOSE 5000

CMD . /venv/bin/activate && /venv/bin/gunicorn -k gevent --reload --workers 2 --worker-connections 5 --access-logfile=- --pythonpath /app
