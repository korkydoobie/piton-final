import sqlite3
from tkinter import messagebox
def connectDb():
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crimes (
            crime_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            crime_name TEXT NOT NULL,
            confinement INTEGER NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            ID INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            crime_Id INTEGER NOT NULL,
            location TEXT NOT NULL,
            date INTEGER NOT NULL,
            mugshot BLOB NOT NULL,
            FOREIGN KEY (crime_Id) REFERENCES crimes(crime_Id)
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
    


#carl methods

def checkExist(criminal_id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM records WHERE ID = (?)",(criminal_id,))
    result = cur.fetchone()

    conn.close()
    return result is not None

def getCriminalData(criminal_id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    cur.execute("SELECT ID, name, crime, location, date FROM records WHERE ID = ?",(criminal_id,))
    result = cur.fetchone()
    conn.close()

    if result:
        ID, name, crime, location, date = result
        return {
        "ID": ID,
        "name": name,
        "crime": crime,
        "location": location,
        "date": date
        }
    else:
        return None
    
def addCriminal(cname):
        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Criminals (name) VALUES (?)", (cname,))
        conn.commit()
        conn.close()
        

def editRecord(criminal_id, criminal_name, criminal_desc, criminal_location, criminal_date):
        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("UPDATE records SET name = ?, crime = ?, location = ?, date = ? WHERE id = ?", (criminal_name, criminal_desc, criminal_location, criminal_date, criminal_id))
        conn.commit()
        conn.close()

def getCriminalList():
     conn = sqlite3.connect("criminal_records.db")
     cur = conn.cursor()
     cur.execute("SELECT name FROM Criminals")
     criminals = [row[0] for row in cur.fetchall()]
     conn.close()

     if not criminals:
          messagebox.showwarning("No criminals found","Criminal list is empty. Please add a criminal first.")
          return None
          
     return criminals     

def getCrimeList():
     conn = sqlite3.connect("criminal_records.db")
     cur = conn.cursor()
     cur.execute("SELECT crime_name FROM crimes")
     crimes = [row[0] for row in cur.fetchall()]
     conn.close()
     return crimes
    #end of carl methods
