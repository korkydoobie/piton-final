import tkinter as tk
from tkinter import messagebox
import sqlite3
import dbs
import random
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import io

class RecordManage:
    def __init__(self, root):
        self.root = root
        self.crimIdentry = tk.StringVar()

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
            crime_dropdown = tk.OptionMenu(frame, criminal_var, *[f"{id} - {name.title()}" for id, name in criminal_list])
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


            date = recordDate.get()
            
            def add_to_db():
                criminal_id = criminal_var.get().strip(" - ")[0] #criminal id
                crime_id = crime_var.get().strip(" - ")[0] # crime id
                location = criminalLocation.get().strip()
                date = recordDate.get().strip()
                
                if criminal_var.get() == "Select Criminal" or crime_var.get() =="Select Crime" or location == "" or date == "":
                    messagebox.showerror("Error", "Please complete the details of the record")
                    return
                
                if not date.isdigit():
                    messagebox.showerror("Invalid date", "Year must be numbers only.")
                
                if (messagebox.askyesno("Confirm Criminal Record Add", "Do you wish to add the criminal record?")):
                    dbs.add_record(criminal_id, crime_id, location, date)
                    messagebox.showinfo("Successful Criminal Record Addition!", "Criminal Record was successfully added!")

                add_window.destroy()

            submit = tk.Button(frame, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black" ,command=add_to_db)
            submit.grid(row=6, column=1, padx=2, pady=10)

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

            tk.Label(search_frame, text="Search Record:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
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
                results = dbs.searchRecords(search_term)  # Get all records
                if results:
                    for row in results:
                        self.tree.insert("", "end", values=(row[6], row[1].title(), row[2].title(), row[3].title(), row[4]))
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

    def handle_search2(self):
        try:
            crime_id = self.crimIdentry.get().strip() #get the inputted sht in the search bar
            print(f"Searching for: {crime_id}")
            
            results = dbs.searchCrime(crime_id) #use the method searchCrime
            print(f"Found {len(results)} records") 
            
            if not results:
                print("No results found")  # Debug print
                self.tree.delete(*self.tree.get_children())
                self.tree.insert("", "end", values=("No records", "", ""))
                return
                
            self.tree.delete(*self.tree.get_children())
            for row in results:
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

    def handle_search(self):
        try:
            criminal_id = self.crimIdentry.get().strip()
            print(f"Searching for: {criminal_id}")
            
            results = dbs.searchRecords(criminal_id)
            print(f"Found {len(results)} records") 
            
            if not results:
                print("No results found")  # Debug print
                self.tree.delete(*self.tree.get_children())
                self.tree.insert("", "end", values=("No records", "", "", "", ""))
                return
                
            self.tree.delete(*self.tree.get_children())
            for row in results:
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            print(f"Database error: {e}")  # Debug print
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("Database error", "", "", "", ""))
        

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
