import sqlite3

def connectDb():
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            ID INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            crime TEXT NOT NULL,
            location TEXT NOT NULL,
            date INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_record(criminal_id, name, crime, location, date):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO records (ID, name, crime, location, date) VALUES (?, ?, ?, ?, ?)", (criminal_id, name, crime, location, date))
    conn.commit()
    conn.close()