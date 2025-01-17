import sqlite3
import os
from datetime import datetime

def convert_apple_timestamp(apple_timestamp):
    """
    Convert Apple Core Data timestamp to human-readable datetime.
    Apple timestamps start from January 1, 2001.
    """
    if apple_timestamp is None:
        return None
    unix_timestamp = apple_timestamp + 978307200  # Convert to Unix epoch
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def query_knowledge_db():
    # Define the path to the KnowledgeC.db file
    db_path = os.path.expanduser("~/Library/Application Support/Knowledge/KnowledgeC.db")
    
    # Initialize connection
    conn = None
    
    # Check if the database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # SQL query to extract app usage data
        query = """
        SELECT 
            ZSTARTDATE, 
            ZENDDATE, 
            ZVALUESTRING AS AppName
        FROM 
            ZOBJECT 
        ORDER BY 
            ZSTARTDATE DESC
        LIMIT 50;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        #print(rows)

        # Print the results in a readable format
        print(f"{'Start Time':<20} {'End Time':<20} {'Duration (s)':<12} {'App Name':<25} {'Bundle ID':<25}")
        print("-" * 100)
        for row in rows:
            start_time = convert_apple_timestamp(row[0])
            end_time = convert_apple_timestamp(row[1])
            app_name = row[2] or "Unknown"
            
            print(f"{start_time:<20} {end_time:<20} {app_name:<25}")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the database connection if it was successfully created
        if conn:
            conn.close()



def test():
    db_path = "file:/Users/alexqin/Library/Application Support/Knowledge/KnowledgeC.db?mode=ro"
    conn = sqlite3.connect(db_path, uri=True)
    print("Connection successful!")
    conn.close()
    


# Run the script
query_knowledge_db()
#test()
