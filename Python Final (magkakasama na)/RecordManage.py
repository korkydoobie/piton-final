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
            criminal_list = dbs.getCriminalList()
        
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
            crime_dropdown = tk.OptionMenu(frame, criminal_var, *[f"{id} - {name}" for id, name in criminal_list])
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
                blobplaceholder = None #temporary

                blobplaceholder = None
                if image_path:
                    with open(image_path, "rb") as file:
                        image_blob = file.read()
                
                if criminal_var.get() == "Select Criminal" or crime_var.get() =="Select Crime" or location == "" or date == "":
                    messagebox.showerror("Error", "Please complete the details of the record")
                    return
                
                if not date.isdigit():
                    messagebox.showerror("Invalid date", "Year must be numbers only.")
                
                if (messagebox.askyesno("Confirm Criminal Record Add", "Do you wish to add the criminal record?")):
                    dbs.add_record(criminal_id, crime_id, location, date, blobplaceholder)
                    messagebox.showinfo("Successful Criminal Record Addition!", "Criminal Record was successfully added!")
                


            submit = tk.Button(frame, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black" ,command=add_to_db)
            submit.grid(row=6, column=1, padx=2, pady=10)

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

    

    def search_criminal_record(self):
        self.root.withdraw()
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("SEARCH CRIMINAL RECORD")
        self.add_window.geometry("800x600+550+100")
        
        self.record_manager = RecordManage(self.root)

        self.crimIdentry = tk.StringVar(value="")

        self.label = tk.Label(self.add_window, text="SEARCH CRIMINAL RECORD", font=("Arial", 20, "bold"))
        self.label.pack(pady=10)
        

        # Entry field for criminal ID search
        
        self.search_entry = tk.Entry(self.add_window, font=("Arial", 14), textvariable=self.crimIdentry)
        self.search_entry.pack(pady=5)

        # Search button
        self.crimIdentry.trace_add("write", lambda *args: self.handle_search())
        self.search_button = tk.Button(self.add_window, text="Search", font=("Arial", 12), command=self.handle_search)
        self.search_button.pack(pady=5)

        # Listbox for search results
        self.results_list = tk.Listbox(self.add_window, font=("Arial", 12), height=6)
        self.results_list.pack(pady=5, fill=tk.BOTH, expand=True)

        # Bind click event to show details
        self.results_list.bind("<<ListboxSelect>>", self.show_details)

        # Label for displaying selected criminal's details
        self.details_label = tk.Label(self.add_window, text="Select a record", font=("Arial", 12), justify="left")
        self.details_label.pack(pady=10)

        self.handle_search()

    def handle_search(self):
        """Fetch records from database and update the listbox."""
        criminal_id = self.crimIdentry.get().strip()
        
        try:
            results = dbs.searchRecords(criminal_id)  # Call the function
        except:
            results = criminal_id.isdigit()

        self.results_list.delete(0, tk.END)  # Clear previous results
        self.details_label.config(text='Select a record')

        if results == False:
            print('INVALID ID')
            self.results_list.insert(tk.END, "Invalid ID")
            return
        elif results:
            for row in results:
                self.results_list.insert(tk.END, f"ID: {row[0]} - {row[1].title()} - {row[2].title()} - {row[3].title()} - {row[4]}")  # ID and Name
        else:
            self.results_list.insert(tk.END, "No results found")
        

    def show_details(self, event):
        """Show full details when a record is selected."""
        selected_index = self.results_list.curselection()
        if not selected_index:
            return
        
        selected_text = self.results_list.get(selected_index[0])
        criminal_id = int(selected_text.split()[1])  # Extract the ID

        # Fetch full details (assuming dbs.searchRecords returns all columns)
        results = dbs.searchRecords(criminal_id)
        if results:
            data = results[0]  # Get first matching record
            details_text = f"ID: {data[0]}\nName: {data[1]}\nCrime: {data[2]}\nLocation: {data[3]}\nArrest: {data[4]}\nRelease: {data[5]}\n"
            self.details_label.config(text=details_text)













'''
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
'''