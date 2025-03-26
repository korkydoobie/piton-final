import tkinter as tk
from tkinter import messagebox
import sqlite3
import dbs

class CrimeManage:
    def __init__(self, root):
        self.root = root

    def add_crime_record(self):
        add_window = tk.Toplevel()
        add_window.title("Add Record")
        add_window.geometry("800x400+550+200")
        add_window.destroy()
        adCrime = tk.Toplevel()
        adCrime.title("Add New Crime ")
        adCrime.geometry("800x800+550+100")
        
        title_label = tk.Label(adCrime, text="ADD NEW CRIME RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.30, y=20)
        
        frame = tk.Frame(adCrime)
        frame.place(relx=0.23, y=100)
        
        tk.Label(frame, text="Crime Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=20, sticky="e")
        crime_name_entry = tk.Entry(frame, width=30, bd=3)
        crime_name_entry.grid(row=1, column=1, padx=2, pady=10)

        tk.Label(frame, text="Crime Sentence: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=20, sticky="e")
        crime_sentence_entry = tk.Entry(frame, width=30, bd=3)
        crime_sentence_entry.grid(row=2, column=1, padx=2, pady=10)

        def confirmAdd():
            crime_name = crime_name_entry.get().strip()
            crime_sentence = crime_sentence_entry.get().strip()
            if not crime_name or not crime_sentence:
                messagebox.showerror("Error", "Crime Name and Crime Sentence cannot be empty!")
                return
        
            if  messagebox.askyesno("Confirm Adding Crime", f"Are you sure you want to add this crime?\nCrime Name: {crime_name}\n Sentence: {crime_sentence}"):
                    dbs.add_crimes(crime_name, crime_sentence)
                    messagebox.showinfo("Success", "New crime record added successfully!")
                    adCrime.destroy()
                
        tk.Button(frame, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=confirmAdd).grid(row=4, column=1, padx=0, pady=20)
        