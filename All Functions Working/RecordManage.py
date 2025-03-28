import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import dbs
import random
from PIL import Image, ImageTk
import io


class RecordManage:
    def __init__(self, root):
        self.root = root
        self.crimIdentry = tk.StringVar()

    def add_record(self):   #update
        if dbs.checkEmpty("criminals") or dbs.checkEmpty("crimes"):
            messagebox.showerror("Missing Data", "Either the Criminals or Crimes table is empty. Please add records first.")
        else:
            criminal_list = dbs.getCriminalList()
        
            self.root.withdraw()
            add_window = tk.Toplevel(self.root)
            add_window.title("Add Record")
            add_window.state('zoomed') 
            title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
            title_label.pack(side="top", pady=10)
            frame = tk.Frame(add_window)
            frame.pack(pady=10)


            # ID 
            tk.Label(frame, text="Enter Criminal ID", font=("Arial", 14, "bold")).pack(pady=10)
            crim_id = tk.Entry(frame, width=30, bd=3, justify="center")
            crim_id.pack(pady=10)

            # Crime
            crime_var = tk.StringVar()
            crime_var.set("Crimes")
            crime_list = dbs.getCrimeList()
            tk.Label(frame, text="Select Crime:", font=("Arial", 14, "bold")).pack(pady=10)
            crime_dropdown = tk.OptionMenu(frame, crime_var, * [f"{id} - {name}" for id, name, _ in crime_list])
            crime_dropdown.pack(pady=10)
            crime_dropdown.config(width=30, bd=3)

            # Location
            tk.Label(frame, text="Enter Location ", font=("Arial", 14, "bold")).pack(pady=10)
            criminalLocation = tk.Entry(frame, width=30, bd=3, justify="center")
            criminalLocation.pack(pady=10)

            # Date
            tk.Label(frame, text="Enter Year of Arrest", font=("Arial", 14, "bold")).pack(pady=10)
            recordDate = tk.Entry(frame, width=30, bd=3, justify="center")
            recordDate.pack(pady=10)

            def add_to_db():
                criminal_id = crim_id.get().strip()  # Criminal ID
                crime_id = crime_var.get().strip(" - ")[0]  # Extract crime ID
                location = criminalLocation.get().strip()
                date = recordDate.get().strip()
                
                if not dbs.searchCriminal(criminal_id):
                    messagebox.showerror("Error", "ID does not exist.")
                    return

                if not criminal_id or crime_var.get() == "Crimes" or not location or not date:
                    messagebox.showerror("Error", "Please complete the details of the record")
                    return

                if not date.isdigit():
                    messagebox.showerror("Invalid date", "Year must be numbers only.")
                    return  # Prevent proceeding with invalid input
                
                if messagebox.askyesno("Confirm Criminal Record Add", "Do you wish to add the criminal record?"):
                    dbs.add_record(criminal_id, crime_id, location, date)
                    messagebox.showinfo("Successful Criminal Record Addition!", "Criminal Record was successfully added!")

                add_window.destroy()

                
            submit = tk.Button(frame, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
            submit.pack(pady=10)
            tk.Label(frame, text="List of Criminals", font=("Arial", 14, "bold")).pack(pady=10)
            
            columns = ("ID", "Name")
            self.criminal_list = ttk.Treeview(add_window, columns=columns, show="headings", height=6)
            self.criminal_list.heading("ID", text="ID")
            self.criminal_list.heading("Name", text="Name")


            self.criminal_list.column("ID", anchor="center")
            self.criminal_list.column("Name", anchor="center")

            self.criminal_list.pack(pady=5, padx=10, fill=tk.BOTH, expand=True, side="top")
            for crim in criminal_list:
                self.criminal_list.insert("", tk.END, values=(crim[0], crim[1]))



    
    def delete_record(self):
        if dbs.checkEmpty("records"):
            messagebox.showerror("Missing Data", "No Records to delete.")
        else:
            delRecord = tk.Toplevel(self.root)
            delRecord.title("Delete Record")
            delRecord.geometry("800x600+550+100")

            title_label = tk.Label(delRecord, text="DELETE RECORD", font=("Arial", 20, "bold"))
            title_label.pack(padx=10, pady=20)

            # Search area
            search_frame = tk.Frame(delRecord)
            search_frame.pack(fill=tk.X, pady=(0, 10))

            tk.Label(search_frame, text="Record ID:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
            search_entry = tk.Entry(search_frame, font=("Arial", 14), textvariable=self.crimIdentry)
            search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Results table
            headers = ["Record ID", "Criminal Name", "Crime", "Location", "Year of Arrest"]
            self.tree = ttk.Treeview(delRecord, columns=headers, show="headings")

            # Configure columns
            col_widths = [80, 150, 150, 150, 100]
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

            def populate_record_list(search_term=""):
                self.tree.delete(*self.tree.get_children())  # Clear existing items
                results = dbs.dynSearch(search_term, "records")  # Get all records
                if results:
                    for row in results:
                        self.tree.insert("", "end", values=(row[0], row[1].title(), row[2].title(), row[3].title(), row[4]))
                else:
                    self.tree.insert("", "end", values=("No records found", "", "", "", ""))

            #call the function to populate the listbox
            populate_record_list()

            # Bind the search entry to the populate_record_list function
            self.crimIdentry.trace_add("write", lambda *args: populate_record_list(self.crimIdentry.get()))

            def delete():
                selected_item = self.tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a record to delete.")
                    return

                selected_record = self.tree.item(selected_item, 'values')
                record_id = selected_record[0]

                if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?"):
                    dbs.deleteRecord(record_id)
                    messagebox.showinfo("Success", "Record deleted successfully!")
                    populate_record_list(self.crimIdentry.get())  # Refresh the list after deletion

            delbtn = tk.Button(delRecord, text="Delete", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
            delbtn.pack(pady=10)
    #END#####

    def search_crime_record(self):
        self.root.withdraw()
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("SEARCH CRIME RECORD")
        self.add_window.geometry("1000x700+400+50")

         # Main container (now with 2 columns)
        main_frame = tk.Frame(self.add_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right column (search + results) - 70% width
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
         
        # ===== RIGHT SIDE: SEARCH + RESULTS ===== 
        # Search area
        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, 
                text="SEARCH CRIME RECORD", 
                font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_entry = tk.Entry(search_frame, 
                                font=("Arial", 14), 
                                textvariable=self.crimIdentry) #for dynamic changes
        self.search_entry.pack(fill=tk.X, pady=5)
        
        # Results table
        headers = ["ID", "Crime Name", "Confinement"]
        self.tree = ttk.Treeview(right_frame, columns=headers, show="headings")
        
        # Configure columns
        col_widths = [80, 150, 150]
        for col, width in zip(headers, col_widths):
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, width=width, anchor='center')
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(right_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        #self.tree.bind("<<TreeviewSelect>>", self.show_details2)
        
        #populate the list
        self.crimIdentry.trace_add("write", lambda *args: self.handle_search2())
        self.handle_search2()

    def handle_search(self):
        try:
            criminal_id = self.crimIdentry.get().strip()
            print(f"Searching for: {criminal_id}")
            
            results2 = dbs.searchRecords(criminal_id)
            print(f"Found {len(results2)} records") 
            
            if not results2:
                print("No results found")  # Debug print
                self.tree.delete(*self.tree.get_children())
                self.tree.insert("", "end", values=("No records", "", "", "", ""))
                return
                
            self.tree.delete(*self.tree.get_children())
            for row in results2:
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            print(f"Database error: {e}")  # Debug print
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("Database error", "", "", "", ""))

    def handle_search2(self):
        try:
            crime_id = self.crimIdentry.get().strip() #get the inputted sht in the search bar
            print(f"Searching for: {crime_id}")
            
            results1 = dbs.searchCrime(crime_id) #use the method searchCrime
            print(f"Found {len(results1)} records") 
            
            if not results1:
                print("No results found")  # Debug print
                self.tree.delete(*self.tree.get_children())
                self.tree.insert("", "end", values=("No records", "", ""))
                return
                
            self.tree.delete(*self.tree.get_children())
            for row in results1:
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            print(f"Database error: {e}")  # Debug print
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("Database error", "", ""))

    def search_criminal_record(self):
        self.root.withdraw()
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("SEARCH CRIMINAL RECORD")
        self.add_window.geometry("1000x700+400+50")  # Larger window for better layout
        
        # Main container (now with 2 columns)
        main_frame = tk.Frame(self.add_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column (image + details) - 30% width
        left_frame = tk.Frame(main_frame, width=300, bg="lightgray")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Right column (search + results) - 70% width
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ===== LEFT SIDE: IMAGE + DETAILS =====
        # Image display
        self.img_frame = tk.Frame(left_frame, bg="white", height=200)
        self.img_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_img = tk.Label(self.img_frame, bg="white")
        self.lbl_img.pack(pady=20, padx=20)
        
        # Details display
        self.details_frame = tk.Frame(left_frame, bg="lightgray")
        self.details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(self.details_frame, 
                                bg="lightgray", 
                                font=("Arial", 12),
                                wrap=tk.WORD,
                                padx=10,
                                pady=10,
                                height=10)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.insert(tk.END, "Select a record to view details")
        self.details_text.config(state=tk.DISABLED)  # Make it read-only
        
        # ===== RIGHT SIDE: SEARCH + RESULTS ===== 
        # Search area
        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, 
                text="SEARCH CRIMINAL RECORD", 
                font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_entry = tk.Entry(search_frame, 
                                font=("Arial", 14), 
                                textvariable=self.crimIdentry)
        self.search_entry.pack(fill=tk.X, pady=5)
        
        # Results table
        headers = ["ID", "Name", "Crime", "Location", "Year"]
        self.tree = ttk.Treeview(right_frame, columns=headers, show="headings")
        
        # Configure columns
        col_widths = [80, 150, 150, 150, 100]
        for col, width in zip(headers, col_widths):
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, width=width, anchor='center')
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(right_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.show_details)
        
        #populate the list
        self.crimIdentry.trace_add("write", lambda *args: self.handle_search())
        self.handle_search()
        

    def show_details(self, event):
        """Show full details when a record is selected."""
        selected_index = self.results_list.curselection()
        if not selected_index:
            return
        
        selected_text = self.results_list.get(selected_index[0])
        
        split_list = selected_text.split(" - ")

        id_value = split_list[0].replace("ID: ", "").strip()  # Remove "ID: "
        first_name = split_list[1].strip()
        crime = split_list[2].strip()
        location = split_list[3].strip()
        date = split_list[4].strip()

        selected = selected_text.split()
        criminal_id = int(selected[1])  # Extract the ID

        # Fetch full details (assuming dbs.searchRecords returns all columns)
        results = dbs.searchRecords(criminal_id)
        
        if results:
            data = results[0]  # Get first matching record
            details_text = f"ID: {id_value}\nName: {first_name.title()}\nCrime: {crime.title()}\nLocation: {location.title()}\nArrest: {date}\nRelease: {data[5]}\n"
            
            imgresults = dbs.searchCriminal(data[0])
            
            img_data = imgresults[2]  # Get BLOB data
            img = Image.open(io.BytesIO(img_data))  # Convert BLOB to an Image
            img = img.resize((100, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible format

            self.lbl.configure(image=img)  # Update the label
            self.lbl.image = img 
            
            self.details_label.config(text=details_text)


    def editRecord(self):
        if dbs.checkEmpty("records"):
            messagebox.showerror("Missing Data", "No Records to edit.")
        else:
            recordList = dbs.getRecordList()
            editRecord = tk.Toplevel(self.root)
            editRecord.title("Edit Record")
            editRecord.state('zoomed')

            title_label = tk.Label(editRecord, text="EDIT RECORD", font=("Arial", 20, "bold"))                
            title_label.pack(padx=10, pady=20)

            frame = tk.Frame(editRecord)
            frame.pack(pady=10)

            self.labelRecord = tk.Label(frame, text="Select a record to edit", font=("Arial", 14, "bold"))
            self.labelRecord.pack(pady=5)

            columns = ("Record ID", "Criminal ID", "Crime ID", "Location", "Year of Arrest", "Year of Release")
            self.record_list = ttk.Treeview(editRecord, columns=columns, show="headings", height=6)
            
            for col in columns:
                self.record_list.heading(col, text=col)
                self.record_list.column(col, anchor="center")

            self.record_list.pack(pady=5, padx=10, fill=tk.BOTH, expand=True, side="top")

            for record in recordList:
                self.record_list.insert("", tk.END, values=(record[0], record[1], record[2], record[3], record[4], record[5]))

            selected_recordId = tk.IntVar()

            def save(event):
                selection = self.record_list.selection()
                if selection:
                    selected_item = self.record_list.item(selection[0], "values")
                    recordId = selected_item[0]
                    selected_recordId.set(recordId)

            self.record_list.bind("<<TreeviewSelect>>", save)

            def edit_crime():
                if not selected_recordId.get():
                    messagebox.showerror("Error", "Choose first.")
                    return

                self.labelRecord.destroy()
                self.submit_button.destroy()
                self.record_list.destroy()

                recordToEdit = dbs.getRecord(selected_recordId.get())
                if not recordToEdit:
                    messagebox.showerror("Error", "Record not found")
                    return

                editId = recordToEdit[0]
                criminal_id = recordToEdit[1]
                crime_id = recordToEdit[2]
                location = recordToEdit[3]
                year_of_arrest = recordToEdit[4]
                year_of_release = recordToEdit[5]
                
                tk.Label(frame, text=f"Record ID ", font=("Arial", 14, "bold")).pack(pady=5)
                recordId_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                recordId_entry.pack(pady=10)
                recordId_entry.insert(0, editId)
                recordId_entry.config(state="disabled")

                tk.Label(frame, text=f"Criminal ID ", font=("Arial", 14, "bold")).pack(pady=5)
                criminal_id_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                criminal_id_entry.pack(pady=10)
                criminal_id_entry.insert(0, criminal_id)
                criminal_id_entry.config(state="disabled")

                tk.Label(frame, text=f"Crime ID ", font=("Arial", 14, "bold")).pack(pady=5)
                crime_id_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                crime_id_entry.pack(pady=10)
                crime_id_entry.insert(0, crime_id)
                crime_id_entry.config(state="disabled")

                tk.Label(frame, text=f"Location ", font=("Arial", 14, "bold")).pack(pady=5)
                location_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                location_entry.pack(pady=10)
                location_entry.insert(0, location)

                year_of_arrest_var = tk.StringVar()
                year_of_arrest_var.set(str(year_of_arrest))
                tk.Label(frame, text=f"Year of Arrest:", font=("Arial", 14, "bold")).pack(pady=5)
                year_of_arrest_entry = tk.Entry(frame, width=30, bd=3, justify="center" ,textvariable=year_of_arrest_var)
                year_of_arrest_entry.pack(pady=10)
           
                tk.Label(frame, text=f"Year of Release", font=("Arial", 14, "bold")).pack(pady=5)
                year_of_release_entry= tk.Entry(frame, width=30, bd=3, justify="center")
                year_of_release_entry.pack(pady=10)
                year_of_release_entry.insert(0, year_of_release)
                year_of_release_entry.config(state="disabled")

                arrestTime = int(year_of_release) - int(year_of_arrest)
                def updateRelease(*args):
                    arrestYear = year_of_arrest_var.get().strip()
                    if arrestYear.isdigit():
                        releaseYear = int(arrestYear) + arrestTime
                        year_of_release_entry.config(state="normal")
                        year_of_release_entry.delete(0, tk.END)
                        year_of_release_entry.insert(0, str(releaseYear))
                        year_of_release_entry.config(state="disabled")

                year_of_arrest_var.trace_add("write", updateRelease)

                def updatedb():
                    arrestYear = year_of_arrest_entry.get()
                    location = location_entry.get()
                    if not location or location.isdigit():
                        messagebox.showerror("Error", "Enter a valid location first.")
                        return
                    if not arrestYear or not arrestYear.isdigit():
                        messagebox.showerror("Error", "Enter a valid year.")
                        return

                    if messagebox.askyesno("Confirm Update", "Do you confirm to update the record?"):
                        messagebox.showinfo("Successfully Updated", "Successfully updated the record!")
                        dbs.editRecord(editId, location, arrestYear)
                        editRecord.destroy()

                updateButton = tk.Button(editRecord, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=updatedb)
                updateButton.pack(pady=10)

            self.submit_button = tk.Button(editRecord, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=edit_crime)
            self.submit_button.pack(pady=10)

    def show_details(self, event):
        selected = self.tree.focus()
        if not selected:
            return
            
        item_data = self.tree.item(selected)['values']
        if not item_data or len(item_data) < 5:
            return
        
        releaseyr = dbs.searchSpecificRecord(item_data[0], item_data[2], item_data[3], item_data[4])
        #returns the tuple of sql which has the value of year release


        #FOR THE PICTURE
        criminal_id = item_data[0]
        criminal_data = dbs.searchCriminal(criminal_id)
        
        if not criminal_data:
            return
        
        # Update details text
        details = (
            f"ID: {item_data[0]}\n\n"
            f"Name: {item_data[1].title()}\n\n"
            f"Crime: {item_data[2].title()}\n\n"
            f"Location: {item_data[3].title()}\n\n"
            f"Arrest Year: {item_data[4]}\n\n"
            f"Release Year: {releaseyr[0]}" #accessing the year release
        )
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
        
        # Update image
        if len(criminal_data) > 2 and criminal_data[2]:
            try:
                img = Image.open(io.BytesIO(criminal_data[2]))
                img = img.resize((200, 200), Image.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)
                
                self.lbl_img.config(image=photo_img)
                self.lbl_img.image = photo_img
            except Exception as e:
                print(f"Image error: {e}")
                self.lbl_img.config(image='')
        else:
            self.lbl_img.config(image='')