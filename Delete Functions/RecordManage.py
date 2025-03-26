import tkinter as tk
from tkinter import messagebox
import sqlite3
import dbs
import random
from tkinter import filedialog
from PIL import Image, ImageTk

class RecordManage:
    def __init__(self, root):
        self.root = root

    def add_record(self):   
        if dbs.checkEmpty("criminals") or dbs.checkEmpty("crimes"):
            messagebox.showerror("Missing Data", "Either the Criminals or Crimes table is empty. Please add records first.")
        else:
            self.root.withdraw()
            add_window = tk.Toplevel(self.root)
            add_window.title("Add Record")
            add_window.geometry("800x400+600+50")

            
            title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
            title_label.place(relx=0.38, y=20)
            
            frame = tk.Frame(add_window)
            frame.place(relx=0.20, y=80)
            
            #Name
            criminal_var = tk.StringVar()
            criminal_var.set("Select Criminal")  # Default value
            criminals_list = dbs.getCriminalList()
            tk.Label(frame, text="Criminal:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
            crime_dropdown = tk.OptionMenu(frame, criminal_var, *[f"{id} - {name}" for id, name in criminals_list])
            crime_dropdown.grid(row=1, column=1, padx=10, pady=10)
            crime_dropdown.config(width=30, bd=3)
            
            #Crime
            crime_var = tk.StringVar()
            crime_var.set("Select Crime")
            crime_list = dbs.getCrimeList()
            tk.Label(frame, text="Crime:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
            crime_dropdown = tk.OptionMenu(frame, crime_var, * [f"{id} - {name}" for id, name in crime_list])
            crime_dropdown.grid(row=2, column=1, padx=10, pady=10)
            crime_dropdown.config(width=30, bd=3)
            
            #Location
            tk.Label(frame, text="Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="w")
            criminalLocation = tk.Entry(frame, width=30, bd=3)
            criminalLocation.grid(row=3, column=1, padx=2, pady=10)
            
            #Date
            tk.Label(frame, text="Year of arrest: ", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="w")
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

            date = recordDate.get()
            
            def add_to_db():
                criminal_id = criminal_var.get().strip(" - ")[0] #criminal id
                crime_id = crime_var.get().strip(" - ")[0]
                location = criminalLocation.get().strip()
                date = recordDate.get().strip()

                image_blob = None
                if image_path:
                    with open(image_path, "rb") as file:
                        image_blob = file.read()
                
                if criminal_var.get() == "Select Criminal" or crime_var.get() =="Select Crime" or location == "" or date == "":
                    messagebox.showerror("Error", "Please complete the details of the record")
                    return
                
                if not date.isdigit():
                    messagebox.showerror("Invalid date", "Year must be numbers only.")
                
                if (messagebox.askyesno("Confirm Criminal Record Add", "Do you wish to add the criminal record?")):
                    dbs.add_record(criminal_id, crime_id, location, date, image_blob)
                    messagebox.showinfo("Successful Criminal Record Addition!", "Criminal Record was successfully added!")

                add_window.destroy()

            submit = tk.Button(frame, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black" ,command=add_to_db)
            submit.grid(row=6, column=1, padx=2, pady=10)
            
###RONNSHITS##############
    def delete_record(self):
        if dbs.checkEmpty("records"):
            messagebox.showerror("Missing Data", "No Records to delete.")
        else:
            delRecord = tk.Toplevel(self.root)
            delRecord.title("Delete Record")
            delRecord.geometry("800x800+550+100")

            title_label = tk.Label(delRecord, text="DELETE RECORD", font=("Arial", 20, "bold"))
            title_label.pack(padx=10, pady=20)

            frame = tk.Frame(delRecord)
            frame.place(relx=0.20, y=80)

            tk.Label(frame, text="Enter Record ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
            record_id_entry = tk.Entry(frame, width=30, bd=3)
            record_id_entry.grid(row=0, column=1, padx=2, pady=10)

            def delete():
                record_id = record_id_entry.get().strip()
                if not record_id:
                    messagebox.showerror("Error", "Please enter a Criminal ID!")
                    return
                
                if dbs.checkExist_records(record_id):
                    dbs.deleteRecord(record_id)
                    messagebox.showinfo("Success", "Record deleted successfully!")
                    delRecord.destroy()
                    
                else:
                    messagebox.showerror("Error", "Failed to delete the record!")

            enter_btn = tk.Button(frame, text="Enter", width=5, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
            enter_btn.grid(row=0, column=3, columnspan=2, padx=20)
#END#####

    def view_criminal_record(self):
        records = dbs.fetchRecords()
        
        if not records:
            messagebox.showerror("No Records", "No criminal records found.")
            
        view_window = tk.Toplevel()
        view_window.title("View Records")
        view_window.geometry("800x300+600+50")
        
        tree = tk.Treeview(view_window, columns=("ID", "Name", "Crime", "Location", "Date"), show="headings")
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