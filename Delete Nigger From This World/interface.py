import tkinter as tk
import random
import dbs
from tkinter import messagebox
import sqlite3

def addRecord():
    add_window = tk.Toplevel()
    add_window.title("Add Record")
    add_window.geometry("800x400+600+50")
    
    title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
    title_label.place(relx=0.38, y=20)
    
    frame = tk.Frame(add_window)
    frame.place(relx=0.20, y=80)
    
    randNum = random.randint(10000, 99999)
    
    #ID
    tk.Label(frame, text="Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    criminalId = tk.Label(frame, text=randNum, font=("Arial", 14, "bold"), width=30).grid(row=0, column=1, padx=10, pady=3)
    
    #Name
    tk.Label(frame, text="Enter Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    criminalName = tk.Entry(frame, width=30, bd=3)
    criminalName.grid(row=1, column=1, padx=2, pady=10)
    
    #Crime
    crime_var = tk.StringVar()
    crime_var.set("None")
    tk.Label(frame, text="Choose Crime: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
    crime_options = ["Murder", "Illegal Drug Trade", "Theft", "Assault", "Fraud", "Domestic Violence", "Slander", "Malicious Mischief", "Cyber Libel", "Identity Theft"]
    crime_dropdown = tk.OptionMenu(frame, crime_var, *crime_options)
    crime_dropdown.grid(row=2, column=1, padx=5, pady=10)
    crime_dropdown.config(width=24, bd=3)
    
    #Location
    tk.Label(frame, text="Enter Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="e")
    criminalLocation = tk.Entry(frame, width=30, bd=3)
    criminalLocation.grid(row=3, column=1, padx=2, pady=10)
    
    #Date
    tk.Label(frame, text="Enter Date(YEAR): ", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="e")
    recordDate = tk.Entry(frame, width=30, bd=3)
    recordDate.grid(row=4, column=1, padx=2, pady=10)
    
    def add_to_db():
        name = criminalName.get().strip()
        crime = crime_var.get().strip()
        location = criminalLocation.get().strip()
        date = recordDate.get().strip()
        
        if name == "" or location == "" or date == "":
            messagebox.showerror("Error", "Name, Location and Date cannot be empty!")
            return
        
        # Get crime_Id from crime_name
        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("SELECT crime_Id FROM crimes WHERE crime_name = ?", (crime,))
        crime_id = cur.fetchone()
        conn.close()
        
        if crime_id:
            dbs.add_record(randNum, name, crime_id[0], location, date, None)
            messagebox.showinfo("Success", "Record added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "Selected crime not found in database!")

    submit = tk.Button(add_window, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
    submit.place(relx=0.4, y=350)

def deleteRecord():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Record")
    delete_window.geometry("800x400+550+200")

    title_label = tk.Label(delete_window, text="DELETE RECORD", font=("Arial", 20, "bold"))
    title_label.place(relx=0.37, y=20)
    
    def delCriminalRecord():
        delete_window.destroy()
        delCriminal = tk.Toplevel()
        delCriminal.title("Delete Criminal Record")
        delCriminal.geometry("800x800+550+200")
        
        title_label = tk.Label(delCriminal, text="DELETE CRIMINAL RECORD", font=("Arial", 20, "bold"))
        title_label.pack(padx=10, pady=20)
        
        frame = tk.Frame(delCriminal)
        frame.place(relx=0.20, y=80)
        
        frame2 = tk.Frame(delCriminal)
        frame2.place(relx=0.20, y=200)
        
        tk.Label(frame, text="Enter Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        criminal_id = tk.Entry(frame, width=30, bd=3)
        criminal_id.grid(row=0, column=1, padx=2, pady=10)
        
        enter = tk.Button(frame, text="Enter", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: showRecord(criminal_id.get().strip(), frame2, delCriminal))    
        enter.grid(row=1, column=1,columnspan=2, padx=2, pady=10)
        
        
    deleteCriminal = tk.Button(delete_window, text="Delete Criminal Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delCriminalRecord)
    deleteCriminal.place(x=250, y=200)
        
    
def showRecord(id, frame, frame2):
    search_result = dbs.search(id)
    if search_result:

        criminalId = search_result[0]
        name = search_result[1]
        crime = search_result[2]
        location = search_result[3]
        date = search_result[4]
        
        tk.Label(frame, text="Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        tk.Label(frame, text=criminalId, font=("Arial", 14, "bold"), width=30).grid(row=0, column=1, padx=10, pady=3)
        
        tk.Label(frame, text="Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        tk.Label(frame, text=name, font=("Arial", 14, "bold"), width=30).grid(row=1, column=1, padx=10, pady=3)
        
        tk.Label(frame, text="Crime: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
        tk.Label(frame, text=crime, font=("Arial", 14, "bold"), width=30).grid(row=2, column=1, padx=10, pady=3)
        
        tk.Label(frame, text="Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="e")
        tk.Label(frame, text=location, font=("Arial", 14, "bold"), width=30).grid(row=3, column=1, padx=10, pady=3)
        
        tk.Label(frame, text="Date: ", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="e")
        tk.Label(frame, text=date, font=("Arial", 14, "bold"), width=30).grid(row=4, column=1, padx=10, pady=3)
        
        tk.Label(frame, text="Are you sure you want to delete this record?", font=("Arial", 14, "bold")).grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="e")
        yes = tk.Button(frame, text="Yes", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: confirm_delete(criminalId, frame, frame2))
        yes.grid(row=6, column=0, padx=5, pady=10)
        
        no = tk.Button(frame, text="No", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: frame2.destroy())
        no.grid(row=6, column=1, padx=5, pady=10)
    else:
        messagebox.showerror("Error", "Record not found in database!")

def confirm_delete(criminalId, frame, frame2):
    if dbs.delete_criminal_record(criminalId):
        messagebox.showinfo("Success", "Record deleted successfully!")
        for widget in frame.winfo_children():
            widget.destroy()
        frame2.destroy()
    else:
        messagebox.showerror("Error", "Failed to delete the record!")
        
        
dbs.connectDb()
dbs.add_crimes()

root = tk.Tk()

root.title("Crime Record Management")
root.geometry("800x600+550+100")

label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
label.pack(padx=10, pady=20)

#Add Record
add = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=addRecord)
add.pack(padx=20, pady=20)

#Edit Record
edit = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
edit.pack(padx=20, pady=20)

#Delete Record
delete = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=deleteRecord)
delete.pack(padx=20, pady=20)

#View Records
logout = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
logout.pack(padx=20, pady=20)

root.mainloop()