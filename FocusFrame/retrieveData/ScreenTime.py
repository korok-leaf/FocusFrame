import sqlite3
import os
from datetime import datetime, timedelta, timezone
import pytz
import random

'''
Screen Time

variables:
most used apps (20)
rows of data

methods:
convert time
process rows
get screen time data

'''



class ScreenTime:

    duration = 2400 # 40 minute intervals

    def __init__(self, start_time, end_time):
        self.apps = {}
        self.start_time = start_time
        self.end_time = end_time

    
    def get_time_mac(self, t):
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
    
    def process_rows(self, rows, duration):
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

            # add to the total used time accross all 40 min intervals

            if name in self.apps:
                self.apps[name] += amount_of_time
            else:
                self.apps[name] = amount_of_time

        screen_off_time = duration-screen_time

        if "off" in self.apps:
            self.apps["off"] += screen_off_time
        else:
            self.apps["off"] = screen_off_time
        
        if screen_off_time > duration//2:
            return "off"
        return max(most_used, key=most_used.get)
        
    
    def get_screen_time_data(self):
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
            
            
            start = self.start_time
            end = self.start_time + duration
            
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
                
                most_used_app = self.process_rows(rows, end-start)
                time_info = self.get_time_mac(start)
                processed.append((most_used_app, time_info))

                variation = random.randint(0, 1200) # 0-20 minutes
                start += duration - variation
                end += duration - variation
                
                if start >= self.end_time: #set later to see if rows is empty
                    break
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            connect.close()
        return processed
     
    def get_app_names(self): # get top 20 names
        top_20 = sorted(self.apps.items(), key=lambda item: item[1], reverse=True)[:20]
        top_20 = list(map(lambda element: element[0], top_20))

        return top_20
    


# testing purposes
test = ScreenTime(758700000, 758990000)

a = test.get_screen_time_data()
#print(a)
print(test.get_app_names())