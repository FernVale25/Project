FROM python:rc-buster

RUN adduser logview

WORKDIR /home/logview


#Necessary for installing everything in requirements.txt
COPY requirements.txt requirements.txt
RUN apt install gcc
RUN apt install make


# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
# You would think the big brains at Microsoft would have made this way easier...
# Or maybe I'm just too dumb to figure out what I need to Google to make this easy
RUN apt --assume-yes update
RUN apt --assume-yes install unixodbc unixodbc-dev libpq-dev
ENV ACCEPT_EULA=Y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

#Configuring the virtual environment
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql 
RUN echo "root:Docker!" | chpasswd 


COPY app app
COPY migrations migrations
COPY LogView.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP LogView.py

RUN chown -R logview:logview ./
USER logview

EXPOSE 5000 80 2222
ENTRYPOINT ["./boot.sh"]