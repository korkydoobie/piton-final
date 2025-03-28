import tkinter as tk
import random
import dbs
from tkinter import messagebox
import sqlite3
from tkinter import filedialog, ttk
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
###RONNSHITS##############
    def delete_criminal_record(self):
        if dbs.checkEmpty("criminals"):
            messagebox.showerror("Missing Data", "No Criminal Records to delete.")
        else:
            delRecord = tk.Toplevel(self.root)
            delRecord.title("Delete Criminal Record")
            delRecord.geometry("800x600+550+100")
            
            self.crimIdentry = tk.StringVar()
            
            title_label = tk.Label(delRecord, text="DELETE CRIMINAL RECORD", font=("Arial", 20, "bold"))
            title_label.pack(padx=10, pady=20)

            # Search area
            search_frame = tk.Frame(delRecord)
            search_frame.pack(fill=tk.X, pady=(0, 10))

            tk.Label(search_frame, text="Search Criminal:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
            search_entry = tk.Entry(search_frame, font=("Arial", 14), textvariable=self.crimIdentry)
            search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Results table
            headers = ["Criminal ID", "Criminal Name"]
            self.tree = ttk.Treeview(delRecord, columns=headers, show="headings")

            # Configure columns
            col_widths = [100, 200]
            for col, width in zip(headers, col_widths):
                self.tree.heading(col, text=col, anchor='center')
                self.tree.column(col, width=width, anchor='center')

            # Add scrollbars
            y_scroll = ttk.Scrollbar(delRecord, orient="vertical", command=self.tree.yview)
            x_scroll = ttk.Scrollbar(delRecord, orient="horizontal", command=self.tree.xview)
            self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

            self.tree.pack(pady=5, fill=tk.BOTH, expand=True)
            y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

            def populate_criminal_list(search_term=""):
                self.tree.delete(*self.tree.get_children())  # Clear existing items
                results = dbs.dynSearch(search_term, "criminals")  # Get all records
                if results:
                    for row in results:
                        self.tree.insert("", "end", values=(row[0], row[1].title()))
                else:
                    self.tree.insert("", "end", values=("No criminal records found", ""))

            #call the function to populate the listbox
            populate_criminal_list()

            # Bind the search entry to the populate_criminal_list function
            self.crimIdentry.trace_add("write", lambda *args: populate_criminal_list(self.crimIdentry.get()))

            def delete():
                selected_item = self.tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a criminal record to delete.")
                    return

                selected_record = self.tree.item(selected_item, 'values')
                criminal_id = selected_record[0]

                if messagebox.askyesno("Confirm Deletion", """Are you sure you want to delete this criminal record?
This action will also delete all the records linked to this criminal."""):
                    dbs.deleteCriminal(criminal_id)
                    messagebox.showinfo("Success", "Criminal Record deleted successfully!")
                    populate_criminal_list(self.crimIdentry.get())  # Refresh the list after deletion

            delbtn = tk.Button(delRecord, text="Delete", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
            delbtn.pack(pady=10)