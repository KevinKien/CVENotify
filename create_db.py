import mysql.connector

# GET MYSQL ENV
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# CONNECT TO MYSQL
connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=MYSQL_DATABASE,
    auth_plugin='mysql_native_password'
)


mycursor = connection.cursor()

mycursor.execute("SHOW TABLES")

for table in mycursor:
    if str(table) != "CVEAppMonitor":
        mycursor.execute("CREATE TABLE CVEAppMonitor (id INT AUTO_INCREMENT PRIMARY KEY, AppName VARCHAR(255) NOT NULL)")

