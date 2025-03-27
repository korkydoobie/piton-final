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
###RONNSHITS##############
    def delete_crime_record(self):
        if dbs.checkEmpty("crimes"):
            messagebox.showerror("Missing Data", "No crime Records to delete.")
        else:
            delRecord = tk.Toplevel(self.root)
            delRecord.title("Delete Crime Record")
            delRecord.geometry("800x800+550+100")
                
            title_label = tk.Label(delRecord, text="DELETE CRIME RECORD", font=("Arial", 20, "bold"))                
            title_label.pack(padx=10, pady=20)

            self.crimIdentry = tk.StringVar()

            tk.Label(delRecord, text="Select a crime to Delete", font=("Arial", 14, "bold")).pack(pady=10)
            search_entry = tk.Entry(delRecord, font=("Arial", 14), textvariable=self.crimIdentry)
            search_entry.pack(pady=10)
                
            crime_list = tk.Listbox(delRecord, font=("Arial", 12), height=6)
            crime_list.pack(pady=5, fill=tk.BOTH, expand=True)
                
            def populate_crime_list(search_term=""):
                crime_list.delete(0, tk.END)  # Clear existing items
                results = dbs.dynSearch(search_term, "crimes")  # Get all records
                if results:
                    for row in results:
                        crime_list.insert(tk.END, f"ID: {row[0]} - {row[1].title()}")
                else:
                    crime_list.insert(tk.END, "No crime records found")

                #call the function to populate the listbox
            populate_crime_list()

                # Bind the search entry to the populate_crime_list function
            self.crimIdentry.trace_add("write", lambda *args: populate_crime_list(self.crimIdentry.get()))
                
            def delete():
                delete_selected = crime_list.curselection()
                if not delete_selected:
                    messagebox.showerror("Error", "Please select a crime record to delete.")
                    return
                        
                delete_selected = crime_list.get(delete_selected[0])
                crime_id = delete_selected.split()[1]
                    
                if messagebox.askyesno("Confirm Deletion", """Are you sure you want to delete this crime record?
This action will also delete all the records linked to this crime."""):
                    dbs.deleteCrime(crime_id)
                    messagebox.showinfo("Success", "Crime Record deleted successfully!")
                    populate_crime_list(self.crimIdentry.get())  # Refresh the list after deletion

            delbtn = tk.Button(delRecord, text="Delete", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
            delbtn.pack(pady=10)
