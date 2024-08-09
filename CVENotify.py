import tweepy
import requests
import os
import mysql.connector
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

# GET MYSQL ENV
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# GET TWITTER ENV
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_COUNT = os.getenv('TWITTER_COUNT')

# GET TELEGRAM
TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# CONNECT TO MYSQL
connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=MYSQL_DATABASE,
    auth_plugin='mysql_native_password'
)
cursor = connection.cursor()

### Ham kiem tra file co ton tai hay khong
def check_file_exits(filename):
    if os.path.exists(filename):
        if os.path.isfile(filename):
            pass
    else:
        f = open(filename, "w")
        f.close()

# Ham send message to Telegram
def send_telegram(msg):
    telegramUrl = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
    requests.post(telegramUrl, json={'text': msg, 'chat_id': TELEGRAM_GROUP_ID})

##### Lay thong tin CVE tu NIST
def getCVEInfo(cvename):
    url = "https://nvd.nist.gov/vuln/detail/" + cvename

    # lay source html
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    page = requests.get(url, headers=headers)
    source = BeautifulSoup(page.content, 'html.parser')

    # Lay description cua lo hong
    Description = source.find('div', class_='col-lg-9 col-md-7 col-sm-12').p.get_text()
    basescore = source.find('span', class_='severityDetail').a.get_text()
    try:
        # Lay thong tin ve diem CVSS
        CVSS = basescore.split(" ")[0]

        # Lay thong tin ve muc do cua lo hong
        Level = basescore.split(" ")[1]
    except:
        # Neu khong co thong tin thi N/A
        CVSS = "N/A"
        Level = "N/A"

    try:
        # Lay thong tin ve attack Vector
        vector = source.find('span', class_='tooltipCvss3NistMetrics').get_text()
        attackvector_raw = vector.split("/")[1]
        if attackvector_raw.split(":")[1] == "N":
            Attackvector = "Network"
        elif attackvector_raw.split(":")[1] == "L":
            Attackvector = "Local"
        elif attackvector_raw.split(":")[1] == "A":
            Attackvector = "Adjacent Network"
        elif attackvector_raw.split(":")[1] == "P":
            Attackvector = "Physical"
    except:
        # Neu khong co thong tin thi N/A
        Attackvector = "N/A"

    return Description, CVSS, Level, Attackvector


# ket noi toi API cua Twitter
authentication = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
authentication.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Main function
for tweet in api.user_timeline(id=TWITTER_USERNAME, count=TWITTER_COUNT):
    # Query appname tu MYSQL
    query_select_app = "select * from CVEAppMonitor"
    cursor.execute(query_select_app)
    # Lay tat ca thong tin tu mysql
    allApps = cursor.fetchall()

    for app in allApps:
        appname = app[1]
        if str(appname.lower()) in tweet.text.lower():
            # kiem tra ID da ton tai trong file cve_sent.txt hay chua
            # Kiem tra file cve_sent.txt ton tai chua, neu chua se tao file cve_sent.txt
            getCurrentDirectory = os.getenv('CURRENTDIRECTORY')
            check_file_exits(getCurrentDirectory + "/cve_sent.txt")
            f_check_send = open(getCurrentDirectory + "/cve_sent.txt", 'r')

            if str(tweet.id) not in f_check_send.read():
                # Lay ma CVE
                cveid = tweet.text.split(" ")[0]

                # Lay CVE info tu NIST
                Description, CVSS, Level, Attackvector = getCVEInfo(cveid)

                # Gui CVE ve Telegram
                msg = "[CVE] APP Name: %s\nCVE: %s\nDescription: %s\nCVSS: %s\nLevel: %s\nAttackvector: %s" % (appname, cveid, Description, CVSS, Level, Attackvector)
                send_telegram(msg)

                # Luu thong tin tweet da gui noti
                file_check = open(getCurrentDirectory + '/cve_sent.txt', 'a+')
                file_check.write(str(tweet.id))
                file_check.write("\n")
                file_check.close()

