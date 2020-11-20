FROM python:rc-buster

RUN adduser logview

WORKDIR /home/logview

COPY requirements.txt requirements.txt
RUN apt install gcc
RUN apt install make
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql


COPY app app
COPY migrations migrations
COPY LogView.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP LogView.py

RUN chown -R logview:logview ./
USER logview

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]