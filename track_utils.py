import sqlite3
import pytz
from datetime import datetime

conn = sqlite3.connect('./data/data.db', check_same_thread=False)
c = conn.cursor()

IST = pytz.timezone('Asia/Kolkata')

# Function to create emotion classifier table
def create_emotionclf_table():
    c.execute('CREATE TABLE IF NOT EXISTS emotionclfTable(rawtext TEXT, prediction TEXT, probability NUMBER, timeOfvisit TIMESTAMP)')

# Function to add prediction details
def add_prediction_details(rawtext, prediction, probability, timeOfvisit=None):
    if timeOfvisit is None:
        timeOfvisit = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    else:
        timeOfvisit = timeOfvisit.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO emotionclfTable(rawtext, prediction, probability, timeOfvisit) VALUES (?, ?, ?, ?)', (rawtext, prediction, probability, timeOfvisit))
    conn.commit()

# Function to view all prediction details
def view_all_prediction_details():
    c.execute('SELECT * FROM emotionclfTable')
    data = c.fetchall()
    return data