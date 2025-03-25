import tkinter as tk
from tkinter import messagebox
import sqlite3
import dbs
import random
from tkinter import filedialog
from PIL import Image, ImageTk


class CriminalManage:
    def __init__(self, root):
        self.root = root

    def add_criminal_record(self):
        self.root.withdraw()
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
        crime_var.set("Murder")
        tk.Label(frame, text="Choose Crime: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
        crime_options = ["Murder", "Illegal Drug Trade", "Theft", "Assault", "Fraud", "Domestic Violence", "Slander", "Malicious Mischief", "Cyber Libel", "Identity Theft"]
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
        
        tk.Label(frame, text="Upload Mugshot: ", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=5, pady=10, sticky="e")
    
        def upload_image():
            global image_path
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path = file_path
                print(f"Selected Image: {file_path}")
            
            
        uploadbtn = tk.Button(frame, text="Browse files", width=26, command=upload_image)
        uploadbtn.grid(row=5, column=1, padx=5, pady=10)
        

        def add_to_db():
            name = criminalName.get().strip()
            crime = crime_var.get().strip()
            location = criminalLocation.get().strip()
            date = recordDate.get().strip()
            image_blob = None

            if name == "" or location == "" or date == "":
                messagebox.showerror("Error", "Name, Location and Date cannot be empty!")
                return
            
            if image_path:
                with open(image_path, "rb") as file:
                    image_blob = file.read()

        
            dbs.add_record(randNum, name, crime, location, date, image_blob)
            messagebox.showinfo("Succes", "Record added successfully!")
            add_window.destroy()
            self.root.deiconify()
        
        #SUUUUUUUUUUBMIT BUTTTONNN
        submit = tk.Button(add_window, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
        submit.place(relx=0.4, y=350)

    def delete_criminal_record(self):
        delCriminal = tk.Toplevel(self.root)
        delCriminal.title("Delete Criminal Record")
        delCriminal.geometry("800x800+550+100")

        title_label = tk.Label(delCriminal, text="DELETE CRIMINAL RECORD", font=("Arial", 20, "bold"))
        title_label.pack(padx=10, pady=20)

        frame = tk.Frame(delCriminal)
        frame.place(relx=0.20, y=80)

        tk.Label(frame, text="Enter Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        criminal_id_entry = tk.Entry(frame, width=30, bd=3)
        criminal_id_entry.grid(row=0, column=1, padx=2, pady=10)

        def delete():
            criminal_id = criminal_id_entry.get().strip()
            if not criminal_id:
                messagebox.showerror("Error", "Please enter a Criminal ID!")
                return

            if dbs.delete_criminal_record(criminal_id):
                messagebox.showinfo("Success", "Record deleted successfully!")
                delCriminal.destroy()
            else:
                messagebox.showerror("Error", "Failed to delete the record!")

        enter_btn = tk.Button(frame, text="Enter", width=5, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
        enter_btn.grid(row=0, column=3, columnspan=2, padx=20)