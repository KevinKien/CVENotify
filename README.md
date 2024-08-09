<h1 align="center">
  Webservice & API IPInfo
</h1>

<h4 align="center"> Identify Geographical Location and Proxy by IP Address </h4>

<p align="center">
  <a href="#install">Install</a> •
  <a href="#api-documentation">Running</a> 
</p>

Webservice and API solution to identify country, region, city, latitude & longitude, ZIP code, time zone, ISP, VPN and residential proxies. IPAddress information is obtained from GeoIP2 and checking IPAddress is proxy or not is obtained from IP2Proxy.com.

## Install
### Install lib python
pip install -r requirements.txt

### Create database with tables
CREATE TABLE CVEAppMonitor (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    AppName varchar(255) NOT NULL
);

### Insert APP Name into table CVEAppMonitor
Example: INSERT INTO CVEAppMonitor (AppName) VALUE ('Billing System Project');

## Running
- Get TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET follow tutorial: https://developer.x.com/en/docs/authentication/oauth-1-0a/api-key-and-secret
# Edit file .env
# Run script python3 getCVETele.py
