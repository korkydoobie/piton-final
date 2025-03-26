import sqlite3
from tkinter import messagebox

def connectDb():
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    
    #creation ng criminals table
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS criminals (
        criminal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        criminal_name TEXT NOT NULL ) """)

    #creation ng crime table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crimes (
            crime_id INTEGER PRIMARY KEY AUTOINCREMENT,
            crime_name TEXT NOT NULL UNIQUE, 
            confinement INTEGER NOT NULL
        )
    """)

    #creation ng records table

    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            criminal_id INTEGER NOT NULL,
            crime_id INTEGER NOT NULL,
            location TEXT NOT NULL,
            year_of_arrest INTEGER NOT NULL,
            year_of_release INTEGER NOT NULL,
            mugshot BLOB NOT NULL,
            FOREIGN KEY (crime_id) REFERENCES crimes(crime_id),
            FOREIGN KEY (criminal_id) REFERENCES criminals(criminal_id)
        )
    """)

    ##auto update nung existing records kapag binago yung confinement years ng crime
    cur.execute("""
            CREATE TRIGGER IF NOT EXISTS update_year_of_release 
            AFTER UPDATE OF confinement ON crimes
            FOR EACH ROW
            BEGIN
                UPDATE records
                SET year_of_release = year_of_arrest + NEW.confinement
                WHERE crime_id = NEW.crime_id;
            END;
        
    """)

    cur.execute("""
            CREATE TRIGGER IF NOT EXISTS update_release_on_arrest_change 
            AFTER UPDATE OF year_of_arrest ON records
            FOR EACH ROW
            BEGIN
                UPDATE records
                SET year_of_release = NEW.year_of_arrest + (SELECT confinement from crimes WHERE crimes.crime_id = NEW.crime_id)
                WHERE record_id = NEW.record_id;
            END;
        
    """)


     
    conn.commit()
    conn.close()
    
    
def add_crimes(cname, time):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO crimes(crime_name, confinement) VALUES (?, ?)",(cname,time))
    conn.commit()
    conn.close()
    
    


#carl methods
def add_record(criminal_id, crime_id, location, date, mugshot): #updated
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    cur.execute("SELECT confinement from crimes WHERE crime_id = ?", (crime_id,))
    result = cur.fetchone()

    if result:
        confinement = result[0]
        releaseDate = int(date) + confinement

        cur.execute("INSERT INTO records (criminal_id, crime_id, location, year_of_arrest, year_of_release, mugshot) VALUES (?, ?, ?, ?, ?, ?)", (criminal_id, crime_id, location, date, releaseDate, mugshot))
        conn.commit()
        conn.close()




###SEARCHING FUNCTIONS#########
def checkEmpty(table_name): #checker if may laman tables
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    conn.close()
    return count == 0

####
####RONSHITS#####
####
#check if a record exists in the table
def checkExist_records(record_id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM records WHERE record_id = (?)",(record_id,))
    result = cur.fetchone()[0]
    if result == 0:
         return None

    conn.close()
    return result is not None

#check if a criminal exists in the table
def checkExist_criminals(criminal_id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM criminals WHERE criminal_id = (?)",(criminal_id,))
    result = cur.fetchone()[0]
    if result == 0:
         return None

    conn.close()
    return result is not None

#check if a crime exists in the table
def checkExist_crimes(crime_id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM crimes WHERE crime_id = (?)",(crime_id,))
    result = cur.fetchone()[0]
    if result == 0:
         return None

    conn.close()
    return result is not None
 
#checks if criminal is available for deletion, if criminal_id is not present in records table
def get_criminals_not_in_records():
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    try:
        # SQL query to find criminals whose IDs are not in the records table
        cur.execute("""
            SELECT criminal_id, criminal_name
            FROM criminals
            WHERE criminal_id NOT IN (SELECT criminal_id FROM records)
        """)
        criminals_not_in_records = cur.fetchall()
        return criminals_not_in_records
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

#checks if crimeis available for deletion, if crime_id is not present in records table
def get_crime_not_in_records():
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()

    try:
        # SQL query to find criminals whose IDs are not in the records table
        cur.execute("""
            SELECT crime_id, crime_name
            FROM crimes
            WHERE crime_id NOT IN (SELECT crime_id FROM records)
        """)
        crime_not_in_records = cur.fetchall()
        return crime_not_in_records
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()
 ####END of RONNSHITS######
######END OF SEARCHING FUNCTIONS##################


# def getCriminalData(criminal_id):
#     conn = sqlite3.connect("criminal_records.db")
#     cur = conn.cursor()

#     cur.execute("SELECT location, year FROM records WHERE ID = ?",(criminal_id,))
#     result = cur.fetchone()
#     conn.close()

#     if result:
#         location, date = result
#         return {
#         "ID": ID,
#         "name": name,
#         "crime": crime,
#         "location": location,
#         "date": date
#         }
#     else:
#         return None
    
def addCriminal(cname):
        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Criminals (criminal_name) VALUES (?)", (cname,))
        conn.commit()
        conn.close()
        
#ronnshits, deletes a row with the matching record_id in the records table
def deleteRecord(id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE record_id = ?", (id,))
    conn.commit()
    conn.close()
    
def deleteCriminal(id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM criminals WHERE criminal_id = ?", (id,))
    conn.commit()
    conn.close()

def deleteCrime(id):
    conn = sqlite3.connect("criminal_records.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM crimes WHERE crime_id = ?", (id,))
    conn.commit()
    conn.close()
#ronnshits END 

def editRecord(record_id, criminal_location, arrest_date): #update mugshot?? di ko alam pano to kirk
        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("UPDATE records SET location = ?, year_of_arrest = ? WHERE id = ?", (criminal_location, arrest_date, record_id))
        conn.commit()
        conn.close()

def getCriminalList():
     conn = sqlite3.connect("criminal_records.db")
     cur = conn.cursor()
     cur.execute("SELECT criminal_id, criminal_name FROM criminals")
     criminals = [(row[0],row[1]) for row in cur.fetchall()] #row - for id, row 1 for criminal name
     conn.close()

     if not criminals:
          messagebox.showwarning("No criminals found","Criminal list is empty. Please add a criminal first.")
          return None
          
     return criminals     

def getCrimeList():
     conn = sqlite3.connect("criminal_records.db")
     cur = conn.cursor()
     cur.execute("SELECT crime_id, crime_name FROM crimes")
     crimes = [(row[0], row[1]) for row in cur.fetchall()] #row 0 for id, row 1 for crime name
     conn.close()
     if not crimes:
          messagebox.showwarning("No crimes found","Crimes list is empty. Please add a crime first.")
          return None
     return crimes


    #end of carl methods
