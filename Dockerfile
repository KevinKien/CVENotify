FROM ubuntu:20.04
LABEL Maintainer="KevinKien"

WORKDIR /cvenotify

COPY . /cvenotify/

RUN apt-get update
RUN apt-get -y install python3 \ 
python3-pip \
cron \
mysql-connector-python

# Set timezon for container
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install package
RUN pip3 install -r requirements.txt --no-cache-dir


# Add the cron job
RUN crontab -l | { cat; echo "* 7 * * * python3 /cvenotify/CVENotify.py"; } | crontab -

# Create table
RUN python3 create_db.py

# Run the command on container startup
CMD cron