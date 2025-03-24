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
            date INTEGER NOT NULL,
            mugshot BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    
def add_crimes():
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    crimes = [
        ('Murder', 20),
        ('Illegal Drug Trade', 12),
        ('Theft', 2),
        ('Assault', 3),
        ('Fraud', 4),
        ('Domestic Violence', 20),
        ('Slander', 2),
        ('Malicious Mischief', 6),
        ('Cyber Libel', 4),
        ('Identity Theft', 7)
    ]
    cur.executemany("INSERT INTO crimes (crime_name, confinement) VALUES (?, ?)", crimes)
    conn.commit()
    conn.close()
    
    
def add_record(criminal_id, name, crime, location, date, mugshot):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO records (ID, name, crime, location, date, mugshot) VALUES (?, ?, ?, ?, ?, ?)", (criminal_id, name, crime, location, date, mugshot))
    conn.commit()
    conn.close()
    
