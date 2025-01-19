import sqlite3
import os


def get_app_name(start, end):
    db_path = os.path.expanduser("~/Library/Application Support/Knowledge/KnowledgeC.db")

    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()

    cursor.execute("""
    SELECT
        ZVALUESTRING
    FROM
        ZOBJECT
    WHERE
        ZSTARTDATE >= ? AND ZENDDATE < ?
    ORDER BY
        ZSTARTDATE
    """, (start, end))  

    rows = cursor.fetchall()

    occur = []

    for row in rows:
        if row[0] in occur:
            continue
        occur.append(row[0])
    
    return occur

print(len(get_app_name(758000000, 758935000)))