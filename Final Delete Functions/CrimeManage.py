import tkinter as tk
from tkinter import messagebox, ttk
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
###RONNSHITS##############
    def delete_crime_record(self):
        if dbs.checkEmpty("crimes"):
            messagebox.showerror("Missing Data", "No crime Records to delete.")
        else:
            delRecord = tk.Toplevel(self.root)
            delRecord.title("Delete Crime Record")
            delRecord.geometry("800x600+550+100")

            title_label = tk.Label(delRecord, text="DELETE CRIME RECORD", font=("Arial", 20, "bold"))
            title_label.pack(padx=10, pady=20)
            
            self.crimIdentry = tk.StringVar()
            
            # Search area
            search_frame = tk.Frame(delRecord)
            search_frame.pack(fill=tk.X, pady=(0, 10))

            tk.Label(search_frame, text="Search Crime:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
            search_entry = tk.Entry(search_frame, font=("Arial", 14), textvariable=self.crimIdentry)
            search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Results table
            headers = ["Crime ID", "Crime Name", "Confinement"]
            self.tree = ttk.Treeview(delRecord, columns=headers, show="headings")

            # Configure columns
            col_widths = [100, 200, 200]
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

            def populate_crime_list(search_term=""):
                self.tree.delete(*self.tree.get_children())  # Clear existing items
                results = dbs.dynSearch(search_term, "crimes")  # Get all records
                if results:
                    for row in results:
                        self.tree.insert("", "end", values=(row[0], row[1].title(), row[2]))
                else:
                    self.tree.insert("", "end", values=("No crime records found", ""))

            #call the function to populate the listbox
            populate_crime_list()

            # Bind the search entry to the populate_crime_list function
            self.crimIdentry.trace_add("write", lambda *args: populate_crime_list(self.crimIdentry.get()))

            def delete():
                selected_item = self.tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a crime record to delete.")
                    return

                selected_record = self.tree.item(selected_item, 'values')
                crime_id = selected_record[0]

                if messagebox.askyesno("Confirm Deletion", """Are you sure you want to delete this crime record?
This action will also delete all the records linked to this crime."""):
                    dbs.deleteCrime(crime_id)
                    messagebox.showinfo("Success", "Crime Record deleted successfully!")
                    populate_crime_list(self.crimIdentry.get())  # Refresh the list after deletion

            delbtn = tk.Button(delRecord, text="Delete", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
            delbtn.pack(pady=10)