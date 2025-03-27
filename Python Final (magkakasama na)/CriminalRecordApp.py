import tkinter as tk
import random
import dbs
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
from CrimeManage import CrimeManage
from CriminalManage import CriminalManage
from RecordManage import RecordManage

class CriminalRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Record Management")
        self.root.geometry("800x600+550+100")
        self.crime_manager = CrimeManage(self.root)
        self.criminal_manager = CriminalManage(self.root)
        self.record_manager = RecordManage(self.root)

        label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
        label.pack(padx=10, pady=20)

        ########################################################################Add Record BUTTON
        self.add_btn = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.add_record)
        self.add_btn.pack(padx=20, pady=20)

        ######################################################################### Edit Record
        self.edit_btn = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
        self.edit_btn.pack(padx=20, pady=20)

        ######################################################################### Delete Record
        self.delete_btn = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.delete_record)
        self.delete_btn.pack(padx=20, pady=20)

        ######################################################################### View Records (Placeholder)
        self.view_btn = tk.Button(root, text="View Records", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", comman=self.view_record)
        self.view_btn.pack(padx=20, pady=20)

        ######################################################################### Logout (Placeholder)
        self.logout_btn = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
        self.logout_btn.pack(padx=20, pady=20)
        
    def add_record(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Record")
        add_window.geometry("800x600+550+200")

        title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.38, y=20)
        ######################################################################## ADD CRIME BUTTON
        tk.Button(add_window, text="Add Crime", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.crime_manager.add_crime_record).place(x=250, y=100)
        ######################################################################## ADD CRIMINAL BUTTON
        tk.Button(add_window, text="Add Criminal", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.criminal_manager.add_criminal).place(x=250, y=200)
        ######################################################################## ADD CRIMINAL BUTTON
        tk.Button(add_window, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.record_manager.add_record).place(x=250, y=300)
        
        tk.Button(add_window, text="Back", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: self.go_back(add_window)).place(x=250, y=400)
        
    def delete_record(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Record")
        delete_window.geometry("800x600+550+200")

        title_label = tk.Label(delete_window, text="DELETE RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.37, y=20)

        tk.Button(delete_window, text="Delete Crime Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.crime_manager.delete_crime_record).place(x=250, y=100)

        tk.Button(delete_window, text="Delete Criminal Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.criminal_manager.delete_criminal_record).place(x=250, y=200)

        tk.Button(delete_window, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.record_manager.delete_record).place(x=250, y=300)

        tk.Button(delete_window, text="Back", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: self.go_back(delete_window)).place(x=250, y=400)
        tk.Button(delete_window, text="Back", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: self.go_back(delete_window)).place(x=250, y=400)
    def view_record(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("View Record")
        delete_window.geometry("800x400+550+200")

        title_label = tk.Label(delete_window, text="VIEW RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.37, y=20)

        tk.Button(delete_window, text="View Crime Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black").place(x=250, y=100)

        tk.Button(delete_window, text="View Criminal Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=self.record_manager.search_criminal_record).place(x=250, y=200)

        tk.Button(delete_window, text="Back", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: self.go_back(delete_window)).place(x=250, y=300)
    
    def go_back(self, window):
        window.destroy()
        self.root.deiconify()
'''
label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
label.pack(padx=10, pady=20)
addCrime = tk.Button(root, text="Add Crime", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", comman=addCrimeRecord)
addCrime.pack(padx=20, pady=20)
addcrim = tk.Button(root, text="Add Criminal", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=addCriminal)
addcrim.pack(padx=20, pady=20)
add = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=addRecord)
add.pack(padx=20, pady=20)
edit = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=editRecord)
edit.pack(padx=20, pady=20)
crimedit = tk.Button(root, text="Edit Crime", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=editCrime)
crimedit.pack(padx=20, pady=20)
delete = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
delete.pack(padx=20, pady=20)
logout = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
logout.pack(padx=20, pady=20)'''