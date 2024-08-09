<h1 align="center">
  CVE Notify
</h1>

<h4 align="center"> Monitor and notify new CVE </h4>

<p align="center">
  <a href="#install">Install</a> •
  <a href="#running">Running</a> 
</p>

CVENotify will fetch the latest CVEs according to your application's and libraries' list and send alerts via Telegram.

## Install
#### Install lib python
```
pip install -r requirements.txt
```

#### Create database with tables
```
CREATE TABLE CVEAppMonitor (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    AppName varchar(255) NOT NULL
);
```

#### Insert APP Name into table CVEAppMonitor
```
Example: INSERT INTO CVEAppMonitor (AppName) VALUE ('Billing System Project');
```

## Running
- Get TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET follow tutorial: https://developer.x.com/en/docs/authentication/oauth-1-0a/api-key-and-secret
- Edit file .env
- Run script
```
python3 getCVETele.py
```
