import sqlite3
import os
from datetime import datetime, timedelta, timezone
import pytz
import random

# convert the mac absolute time into
def get_time_mac(t):
    apple_epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)
    utc_datetime = apple_epoch + timedelta(seconds=t)

    # Convert to Toronto timezone
    toronto_tz = pytz.timezone("America/Toronto")
    toronto = utc_datetime.astimezone(toronto_tz)
    
    yea = toronto.year
    mon = toronto.month
    h = toronto.hour
    m = toronto.minute
    s = toronto.second
    
    day_of_week = (1+toronto.weekday())%7 # weekday
    
    return (yea, mon, h, m, s, day_of_week)


# rows = (start_time, end_time, name)
def process_rows(rows, duration):
    
    # process logic
    # for every 40 min intervals we select the app that has been used the largest amount of time
    l = len(rows)
    
    most_used = {} # dictionary
    screen_time = 0
    
    for i in range(l):
        element = rows[i]
        start = element[0]
        end = element[1]
        name = element[2]
        
        amount_of_time = abs(end-start)
        if name == None:
            continue
        
        screen_time += amount_of_time
        if name in most_used:
            most_used[name] += amount_of_time
        else:
            most_used[name] = amount_of_time
    
    screen_off_time = duration-screen_time
    
    if screen_off_time > duration//2:
        return "off"
    return max(most_used, key=most_used.get)
    


def get_screen_time_data(start_time, end_time):
    db_path = os.path.expanduser("~/Library/Application Support/Knowledge/KnowledgeC.db")
    
    connect = None

    duration = 2400 # 40 minute intervals
    processed = []
    
    if not os.path.exists(db_path):
        print("does not exist")
        return
    
    try:
        connect = sqlite3.connect(db_path)
        cursor = connect.cursor()
        
        
        start = start_time
        end = start_time + duration
        
        while True:
            connect = sqlite3.connect(db_path)
            cursor = connect.cursor()
            
            cursor.execute("""
            SELECT
                ZSTARTDATE,
                ZENDDATE,
                ZVALUESTRING
            FROM
                ZOBJECT
            WHERE
                ZSTARTDATE >= ? AND ZENDDATE < ?
            ORDER BY
                ZSTARTDATE
            """,(start, end))
            
            rows = cursor.fetchall()

            
            
            most_used_app = process_rows(rows, end-start)
            time_info = get_time_mac(start)
            processed.append((most_used_app, time_info))

            variation = random.randint(0, 1200) # 0-20 minutes
            start += duration - variation
            end += duration - variation
            
            if start >= end_time: #set later to see if rows is empty
                break
        
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connect.close()
    return processed

#get_screen_time_data(758837705, 758869734)
#print("-----------------------")
#get_screen_time_data(758850564, 0)
#print("done")
