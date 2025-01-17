import sqlite3
import os
from datetime import datetime

def get_screen_time_data():
    db_path = os.path.expanduser("~/Library/Application Support/Knowledge/KnowledgeC.db")
    
    connect = None
    
    if not os.path.exists(db_path):
        print("does not exist")
        return;
    
    try:
        connect = sqlite3.connect(db_path)
        cursor = connect.cursor()
        
        sql = """
        SELECT 
            ZSTARTDATE, 
            ZENDDATE, 
            ZVALUESTRING AS AppName
        FROM 
            ZOBJECT
        WHERE
            ZSTARTDATE >= 758837705
        ORDER BY 
            ZSTARTDATE DESC
        LIMIT 100;
        """
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")

get_screen_time_data()
