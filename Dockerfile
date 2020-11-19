FROM python:rc-buster

RUN mkdir -p ./dockerapp/src

WORKDIR /app/src

RUN pip install flask-wtf
RUN pip install flask-sqlalchemy
RUN pip install flask-migrate
RUN pip install flask-login
RUN pip install email-validator
RUN pip install flask-bootstrap
RUN pip install flask-moment

COPY . /dockerapp/src

EXPOSE 5000

ENV FLASK_DEBUG=1
ENV FLASK_APP=1

CMD ["flask", "run", "-h", "0.0.0.0"]