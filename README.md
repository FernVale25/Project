To run this in docker, execute the following:

docker build -t logview:latest
(This builds the docker container)


docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=logview -e MYSQL_USER=logview -e MYSQL_PASSWORD=aaa mysql/mysql-server:5.7 
(This starts the database)

docker run --name logview -p 8000:5000 --rm --link mysql:dbserver -e DATABASE_URL=mysql+pymysql://logview:aaa@dbserver/logview logview:latest
(This starts the webservice)