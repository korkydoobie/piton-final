import tkinter as tk
from tkinter import messagebox
import sqlite3
import dbs

class CrimeManage:
    def __init__(self, root):
        self.root = root

    def add_crime_record(self):
        adCrime = tk.Toplevel(self.root)
        adCrime.title("Add New Crime Record")
        adCrime.geometry("800x800+550+100")

        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("SELECT MAX(crime_Id) FROM crimes")
        last_crime_id = cur.fetchone()[0]
        next_crime_id = last_crime_id + 1 if last_crime_id else 1
        conn.close()

        title_label = tk.Label(adCrime, text="ADD NEW CRIME RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.30, y=20)

        frame = tk.Frame(adCrime)
        frame.place(relx=0.23, y=100)

        tk.Label(frame, text="Crime ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=20, sticky="e")
        tk.Label(frame, text=next_crime_id, font=("Arial", 14, "bold")).grid(row=0, column=1, padx=20, pady=3)

        tk.Label(frame, text="Crime Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=20, sticky="e")
        crime_name_entry = tk.Entry(frame, width=30, bd=3)
        crime_name_entry.grid(row=1, column=1, padx=2, pady=10)

        tk.Label(frame, text="Crime Sentence: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=20, sticky="e")
        crime_sentence_entry = tk.Entry(frame, width=30, bd=3)
        crime_sentence_entry.grid(row=2, column=1, padx=2, pady=10)

        def confirm_add():
            crime_name = crime_name_entry.get().strip()
            crime_sentence = crime_sentence_entry.get().strip()

            if not crime_name or not crime_sentence:
                messagebox.showerror("Error", "Crime Name and Crime Sentence cannot be empty!")
                return

            dbs.add_crime_record(next_crime_id, crime_name, crime_sentence)
            messagebox.showinfo("Success", "New crime record added successfully!")
            adCrime.destroy()

        tk.Button(frame, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=confirm_add).grid(row=4, column=1, padx=0, pady=20)

    