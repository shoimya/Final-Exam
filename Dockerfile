# Author  : Prof. MM Ghassemi <ghassem3@msu.edu>
# Access instance using `docker exec -it exam-container_flask-app bash`

# Instantiate Ubuntu 20.04
FROM ubuntu:20.04
LABEL maintainer "Mohammad Ghassemi <ghassem3@msu.edu>"
LABEL description="This is custom Docker Image for Dr. Ghassemi's Web Application Course"

# Update Ubuntu Software repository
RUN apt update
RUN apt-get update -qq

# Install MySQL and create the database
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y mysql-server 
RUN service mysql start && mysql -e "CREATE USER 'master'@'localhost' IDENTIFIED BY 'master';CREATE DATABASE db; GRANT ALL PRIVILEGES ON db.* TO 'master'@'localhost';"
#RUN service mysql start && mysql -e "CREATE USER 'master'@'localhost' IDENTIFIED BY 'master';CREATE DATABASE db; GRANT SUPER ON *.* TO 'master'@'localhost';"

# Add the Flask application and install requirements
RUN apt -y install python3-pip
RUN apt -y install vim
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Open ports, set environment variables, start the application.
EXPOSE 8080 
ENV PORT 8080

#EXPOSE 3336 
#ENV PORT 3336

ENV FLASK_ENV=development
CMD service mysql start && exec python3 app.py
# ----------------------------------------------------- 
