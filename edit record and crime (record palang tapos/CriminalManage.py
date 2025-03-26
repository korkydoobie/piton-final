import tkinter as tk
import random
import dbs
from tkinter import messagebox
import sqlite3
from tkinter import filedialog
from PIL import Image, ImageTk

class CriminalManage:
    def __init__(self, root):
        self.root = root

    def add_criminal(self):
        criminal_window = tk.Toplevel()
        criminal_window.title("Add Record")
        criminal_window.geometry("800x400+600+50")

        title_label = tk.Label(criminal_window, text="Add Criminal", font=("Arial", 20, "bold"))
        title_label.place(relx=0.35, y=20)
        frame = tk.Frame(criminal_window)
        frame.place(relx=0.20, y=80)

        tk.Label(frame, text="Enter Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        criminalName = tk.Entry(frame, width=30, bd=3)
        criminalName.grid(row=1, column=1, padx=2, pady=10)

        tk.Label(frame, text="Upload Mugshot: ", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=5, pady=10, sticky="e")
        
        def upload_image():
            global image_path
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path = file_path
                print(f"Selected Image: {file_path}")
                
                
        uploadbtn = tk.Button(frame, text="Browse files", width=26, command=upload_image)
        uploadbtn.grid(row=5, column=1, padx=5, pady=10)

        def submitEdit():
            image_blob = None
            if image_path:
                with open(image_path, "rb") as file:
                    image_blob = file.read()

            name = criminalName.get().strip()
            if messagebox.askyesno("Confirm Addition of Criminal", f"Do you wish to add {name} in the criminal list?"):
                dbs.addCriminal(name, image_blob)
                messagebox.showinfo("Criminal Addition Success", f"{name} was added to the criminal list.")
                criminal_window.destroy()
            

        criminalAdd = tk.Button(frame, text="Add Criminal", font=("Arial", 10, "bold"), command=submitEdit)
        criminalAdd.grid(row=10, column=1, padx=10,columnspan=2, pady=10, sticky="nw")




