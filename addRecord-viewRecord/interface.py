import tkinter as tk
import random
import dbs
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk


def addRecord(add_choices_window):
    add_choices_window.destroy()
    add_window = tk.Toplevel()
    add_window.title("Add Record")
    add_window.geometry("800x500+600+50")
    
    title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
    title_label.place(relx=0.38, y=20)
    
    frame = tk.Frame(add_window)
    frame.place(relx=0.20, y=80)
    
    randNum = random.randint(100, 999)
    
    #ID
    tk.Label(frame, text="Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    criminalId = tk.Label(frame, text=randNum, font=("Arial", 14, "bold"), width=30).grid(row=0, column=1, padx=10, pady=3)
    
    #Name
    tk.Label(frame, text="Enter Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    criminalName = tk.Entry(frame, width=30, bd=3)
    criminalName.grid(row=1, column=1, padx=2, pady=10)
    
    #Crime
    crime_var = tk.StringVar()
    crime_var.set("Murder")
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
        
        if name == "" or location == "" or date == "":
            messagebox.showerror("Error", "Name, Location and Date cannot be empty!")
            return
        
        image_blob = None
        if image_path:
            with open(image_path, "rb") as file:
                image_blob = file.read()
        
        dbs.add_record(randNum, name, crime, location, date, image_blob)
        messagebox.showinfo("Succes", "Record added successfully!")
        add_window.destroy()
        root.deiconify()

    submit = tk.Button(add_window, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
    submit.place(relx=0.4, y=400)
    

def add_choices():
    root.withdraw()
    add_choices_window = tk.Toplevel()
    add_choices_window.title("Add Record")
    add_choices_window.geometry("800x300+600+50")
    
    frame = tk.Frame(add_choices_window)
    frame.place(relx=0.28, y=100)
    
    title_label = tk.Label(add_choices_window, text="WHAT WOULD YOU LIKE TO ADD?", font=("Arial", 20, "bold"))
    title_label.place(relx=0.21, y=20)
    
    criminal = tk.Button(frame, text="Criminal Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: addRecord(add_choices_window))
    criminal.pack(padx=20, pady=20)
    crime = tk.Button(frame, text="Crime", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
    crime.pack(padx=20, pady=20)

def view_records():
    records = dbs.fetchRecords()
    
    if not records:
        messagebox.showerror("No Records", "No criminal records found.")
        
    view_window = tk.Toplevel()
    view_window.title("View Records")
    view_window.geometry("800x300+600+50")
    
    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Crime", "Location", "Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Crime", text="Crime")
    tree.heading("Location", text="Location")
    tree.heading("Date", text="Date")
    
    tree.column("ID", width=80, anchor="center")
    tree.column("Name", width=200, anchor="center")
    tree.column("Crime", width=200, anchor="center")
    tree.column("Location", width=200, anchor="center")
    tree.column("Date", width=100, anchor="center")
    
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    for record in records:
        tree.insert("", "end", values=record)
    
    close_button = tk.Button(view_window, text="Close", command=view_window.destroy)
    close_button.pack(pady=10)

dbs.connectDb()

root = tk.Tk()
root.title("Interface")
root.geometry("800x500+600+50")


label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
label.pack(padx=10, pady=20)
add = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_choices)
add.pack(padx=20, pady=20)
edit = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
edit.pack(padx=20, pady=20)
view = tk.Button(root, text="View Records", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=view_records)
view.pack(padx=20, pady=20)
delete = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
delete.pack(padx=20, pady=20)
logout = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
logout.pack(padx=20, pady=20)

root.mainloop()