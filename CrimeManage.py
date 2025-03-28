import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import dbs

class CrimeManage:
    def __init__(self, root):
        self.root = root

    def add_crime_record(self):
        adCrime = tk.Toplevel()
        adCrime.title("Add New Crime ")
        adCrime.state('zoomed') 
        
        title_label = tk.Label(adCrime, text="ADD NEW CRIME RECORD", font=("Arial", 20, "bold"))
        title_label.pack(pady= 10, side="top")

        frame = tk.Frame(adCrime)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Crime Name: ", font=("Arial", 14, "bold")).pack()
        crime_name_entry = tk.Entry(frame, width=30, bd=3, justify="center")
        crime_name_entry.pack(pady=10)

        tk.Label(frame, text="Crime Sentence: ", font=("Arial", 14, "bold")).pack()
        crime_sentence_entry = tk.Entry(frame, width=30, bd=3, justify="center")
        crime_sentence_entry.pack(pady=10)

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
        tk.Button(frame, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=confirmAdd).pack(pady=10)
       
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

            tk.Label(search_frame, text="Crime ID:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
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

    def editCrime(self):
        if dbs.checkEmpty("crimes"):
            messagebox.showerror("Missing Data", "No crime Records to edit.")
        else:
            crimeList = dbs.getCrimeList()
            editRecord = tk.Toplevel(self.root)
            editRecord.title("Edit Crime Record")
            editRecord.state('zoomed')

            title_label = tk.Label(editRecord, text="EDIT CRIME RECORD", font=("Arial", 20, "bold"))
            title_label.pack(padx=10, pady=20)

            frame = tk.Frame(editRecord)
            frame.pack(pady=10)

            self.labelCrime = tk.Label(frame, text="Select a crime to edit", font=("Arial", 14, "bold"))
            self.labelCrime.pack(pady=5)
            
            # Creating the Treeview
            columns = ("ID", "Crime Name", "Confinement Years")
            self.crime_tree = ttk.Treeview(editRecord, columns=columns, show="headings")
            self.crime_tree.heading("ID", text="ID")
            self.crime_tree.heading("Crime Name", text="Crime Name")
            self.crime_tree.heading("Confinement Years", text="Confinement Years")

            self.crime_tree.column("ID", anchor="center")
            self.crime_tree.column("Crime Name", anchor="center")
            self.crime_tree.column("Confinement Years", anchor="center")

            self.crime_tree.pack(pady=5,fill=tk.BOTH, expand=True)
            
            for crime in crimeList:
                self.crime_tree.insert("", "end", values=(crime[0], crime[1], crime[2]))
            
            selected_crimeId = tk.IntVar()
            
            def select_item(event):
                selected = self.crime_tree.selection()
                if selected:
                    crimeId = self.crime_tree.item(selected[0], "values")[0]
                    selected_crimeId.set(crimeId)
            
            self.crime_tree.bind("<<TreeviewSelect>>", select_item)
            
            def edit_crime():
                if not selected_crimeId.get():
                    messagebox.showerror("Error", "Choose a crime first.")
                    return
                
                self.labelCrime.destroy()
                self.submit_button.destroy()
                self.crime_tree.destroy()
                
                crimeToEdit = dbs.getCrime(selected_crimeId.get())
                editId, editName, editConfinement = crimeToEdit

                tk.Label(frame, text="Crime ID", font=("Arial", 14, "bold")).pack(pady=10)
                crime_id_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                crime_id_entry.pack(pady=10)
                crime_id_entry.insert(0, editId)
                crime_id_entry.config(state="disabled")
                
                tk.Label(frame, text="Crime Name", font=("Arial", 14, "bold")).pack(pady=5)
                crime_name_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                crime_name_entry.pack(pady=10)
                crime_name_entry.insert(0, editName)
                
                tk.Label(frame, text="Years of Confinement", font=("Arial", 14, "bold")).pack(pady=5)
                crime_confinement_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                crime_confinement_entry.pack(pady=10)
                crime_confinement_entry.insert(0, editConfinement)
                
                
                def updatedb():
                    crimeName = crime_name_entry.get()
                    confinement = crime_confinement_entry.get()
                    
                    if not crimeName or crimeName.isdigit():
                        messagebox.showerror("Error", "Enter a valid crime name.")
                        return
                    if not confinement.isdigit():
                        messagebox.showerror("Error", "Enter a valid number for years.")
                        return
                    
                    if messagebox.askyesno("Confirm Update", "Do you confirm to update the crime?"):
                        dbs.editCrime(editId, crimeName, confinement)
                        messagebox.showinfo("Successfully Updated", "Crime record updated successfully!")
                        editRecord.destroy()
                
                updateButton = tk.Button(editRecord, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=updatedb)
                updateButton.pack(pady=10)
            
            self.submit_button = tk.Button(editRecord, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=edit_crime)
            self.submit_button.pack(pady=10)

                
                





