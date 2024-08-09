# Install lib python
pip install -r requirements.txt

# Create database with tables
CREATE TABLE CVEAppMonitor (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    AppName varchar(255) NOT NULL
);

# Insert APP Name into table CVEAppMonitor
Example: INSERT INTO CVEAppMonitor (AppName) VALUE ('Billing System Project');

# Edit file .env
# Run script python3 getCVETele.py