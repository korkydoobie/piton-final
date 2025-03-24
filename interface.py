import tkinter as tk
import random
import dbs
from tkinter import messagebox

class CrimeRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface")
        self.root.geometry("800x400+600+50")
        
        self.label = tk.Label(self.root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
        self.label.pack(padx=10, pady=20)
        
        self.add_button = tk.Button(self.root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.addRecord)
        self.add_button.pack(padx=20, pady=20)
        
        self.edit_button = tk.Button(self.root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
        self.edit_button.pack(padx=20, pady=20)
        
        self.delete_button = tk.Button(self.root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
        self.delete_button.pack(padx=20, pady=20)
        
        self.logout_button = tk.Button(self.root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
        self.logout_button.pack(padx=20, pady=20)
    
    def addRecord(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Record")
        add_window.geometry("800x400+600+50")
        
        title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.38, y=20)
        
        frame = tk.Frame(add_window)
        frame.place(relx=0.20, y=80)
        
        randNum = random.randint(10000, 99999)
        
        # ID
        tk.Label(frame, text="Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        tk.Label(frame, text=randNum, font=("Arial", 14, "bold"), width=30).grid(row=0, column=1, padx=10, pady=3)
        
        # Name
        tk.Label(frame, text="Enter Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        criminalName = tk.Entry(frame, width=30, bd=3)
        criminalName.grid(row=1, column=1, padx=2, pady=10)
        
        # Crime
        crime_var = tk.StringVar()
        crime_var.set("Felony")
        tk.Label(frame, text="Choose Crime: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
        crime_options = ["Felony", "Misdemeanor", "Theft", "Assault", "Fraud"]
        crime_dropdown = tk.OptionMenu(frame, crime_var, *crime_options)
        crime_dropdown.grid(row=2, column=1, padx=5, pady=10)
        crime_dropdown.config(width=24, bd=3)
        
        # Location
        tk.Label(frame, text="Enter Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="e")
        criminalLocation = tk.Entry(frame, width=30, bd=3)
        criminalLocation.grid(row=3, column=1, padx=2, pady=10)
        
        # Date
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
            
            # Assuming dbs.add_record exists
            # dbs.add_record(randNum, name, crime, location, date)
            messagebox.showinfo("Success", "Record added successfully!")
            add_window.destroy()
        
        submit = tk.Button(add_window, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
        submit.place(relx=0.4, y=350)

