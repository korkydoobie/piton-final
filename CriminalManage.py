import tkinter as tk
import random
import io
import dbs
from tkinter import messagebox, filedialog, ttk
import sqlite3
from PIL import Image, ImageTk
class CriminalManage:
    def __init__(self, root):
        self.root = root

    def add_criminal(self):
        global image_path, img_label
        image_path = None
        criminal_window = tk.Toplevel()
        criminal_window.title("Add Record")
        criminal_window.state('zoomed') 

        title_label = tk.Label(criminal_window, text="Add Criminal", font=("Arial", 20, "bold"))
        title_label.pack(pady=20, side="top")

        frame = tk.Frame(criminal_window)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Enter Name: ", font=("Arial", 14, "bold")).pack()
        criminalName = tk.Entry(frame, width=30, bd=3, justify="center")
        criminalName.pack(pady=10)

        
        tk.Label(frame, text="Upload Mugshot: ", font=("Arial", 14, "bold")).pack()
        
        img_label = tk.Label(frame)
        img_label.pack(pady=10)
        def upload_image():
            global image_path 
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path = file_path
                

                img = Image.open(image_path)
                img = img.resize((150, 150))

                img_tk = ImageTk.PhotoImage(img)
                img_label.config(image=img_tk)
                img_label.image = img_tk
                print(f"Selected Image: {file_path}")
                
                
                
        uploadbtn = tk.Button(frame, text="Browse files", width=26, command=upload_image)
        uploadbtn.pack(pady=10)

        def submitEdit():
            global image_path
            name = criminalName.get().strip()
            if name == "":  
                 messagebox.showerror("Error", "Please enter a name.")
                 return
            if image_path is None:
                messagebox.showerror("Error", "Please upload a mugshot before adding the criminal.")
                return
            else:
                with open(image_path, "rb") as file:
                        image_blob = file.read()
                    
            if messagebox.askyesno("Confirm Addition of Criminal", f"Do you wish to add {name} in the criminal list?"):
                dbs.addCriminal(name, image_blob)
                messagebox.showinfo("Criminal Addition Success", f"{name} was added to the criminal list.")
                criminal_window.destroy()
            

        criminalAdd = tk.Button(frame, text="Add Criminal", font=("Arial", 10, "bold"), command=submitEdit)
        criminalAdd.pack(pady=10)
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

            tk.Label(search_frame, text="Criminal ID:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
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



    def editCriminal(self):
        if dbs.checkEmpty("criminals"):
            messagebox.showerror("Missing Data", "No Criminal Records to edit.")
        else:
            criminalList = dbs.getCriminalList()
            editRecord = tk.Toplevel(self.root)
            editRecord.title("Edit Criminal Record")
            editRecord.state('zoomed')

            title_label = tk.Label(editRecord, text="EDIT CRIMINAL RECORD", font=("Arial", 20, "bold"))                
            title_label.pack(padx=10, pady=20)

            frame = tk.Frame(editRecord)
            frame.pack(pady=10)

            self.labelCriminal = tk.Label(frame, text="Select a Criminal to edit", font=("Arial", 14, "bold"))
            self.labelCriminal.pack(pady=5)

            columns = ("ID", "Name")
            self.criminal_list = ttk.Treeview(editRecord, columns=columns, show="headings", height=6)
            self.criminal_list.heading("ID", text="ID")
            self.criminal_list.heading("Name", text="Name")
            self.criminal_list.column("ID", anchor="center")
            self.criminal_list.column("Name", anchor="center")
            self.criminal_list.pack(pady=5, padx=10, fill=tk.BOTH, expand=True, side="top")

            for criminal in criminalList:
                self.criminal_list.insert("", tk.END, values=(criminal[0], criminal[1]))

            selected_criminalId = tk.IntVar()

            def save(event):
                selection = self.criminal_list.selection()
                if selection:
                    selected_item = self.criminal_list.item(selection[0], "values")
                    criminalId = selected_item[0]
                    selected_criminalId.set(criminalId)

            self.criminal_list.bind("<<TreeviewSelect>>", save)

            def edit_criminal():
                if not selected_criminalId.get():
                    messagebox.showerror("Error", "Choose first.")
                    return

                self.labelCriminal.destroy()
                self.submit_button.destroy()
                self.criminal_list.destroy()
                criminalToEdit = dbs.getCriminal(selected_criminalId.get())

                if not criminalToEdit:
                    messagebox.showerror("Error", "Criminal not found")
                    return

                editId = criminalToEdit[0]
                editName = criminalToEdit[1]
                editMugshot = criminalToEdit[2]

                tk.Label(frame, text=f"Criminal ID ", font=("Arial", 14, "bold")).pack(pady=5)
                criminal_id_entry = tk.Entry(frame, width=30, bd=3, justify="center")
                criminal_id_entry.pack(pady=10)
                criminal_id_entry.insert(0, editId)
                criminal_id_entry.config(state="disabled")

                tk.Label(frame, text=f"Criminal Name ", font=("Arial", 14, "bold")).pack(pady=5)
                criminal_name_entry = tk.Entry(frame, width=30, bd=3  ,justify="center")
                criminal_name_entry.pack(pady=10)
                criminal_name_entry.insert(0, editName)

                if editMugshot:
                    try:
                        tk.Label(frame, text=f"Criminal Mugshot ", font=("Arial", 14, "bold")).pack(pady=5)
                        img = Image.open(io.BytesIO(editMugshot))  # Convert BLOB to an Image
                        img = img.resize((150, 150), Image.LANCZOS)  # Resize to fit
                        img = ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible format
                        
                        self.img_label = tk.Label(frame, image=img)
                        self.img_label.image = img  # Keep reference to avoid garbage collection
                        self.img_label.pack(pady=10)

                        def upload_image():
                            global image_path
                            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
                            if file_path:
                                image_path = file_path
                                new_img = Image.open(image_path)
                                new_img = new_img.resize((150, 150), Image.LANCZOS)
                                new_img = ImageTk.PhotoImage(new_img)
                                self.img_label.configure(image=new_img)
                                self.img_label.image = new_img  # Keep reference to avoid garbage collection

                        uploadbtn = tk.Button(frame, text="Upload New Picture", width=26, command=upload_image)
                        uploadbtn.pack(pady=10)
                    except Exception as e:
                        messagebox.showerror("Image Error", f"Failed to load image: {e}")

                def updatedb():
                    global image_path
                    criminalName = criminal_name_entry.get()
                    if not criminalName or criminalName.isdigit():
                        messagebox.showerror("Error", "Enter a valid name first.")
                        return

                    if image_path:
                        with open(image_path, "rb") as file:
                            updated_mugshot = file.read()
                    else:
                        updated_mugshot = editMugshot

                    if messagebox.askyesno("Confirm Update", f"Do you confirm to update the criminal?"):
                        messagebox.showinfo("Successfully Updated", "Successfully updated the Criminal!")
                        dbs.editCriminal(editId, criminalName, updated_mugshot)
                        editRecord.destroy()

                updateButton = tk.Button(editRecord, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=updatedb)
                updateButton.pack(pady=10)

            self.submit_button = tk.Button(editRecord, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=edit_criminal)
            self.submit_button.pack(pady=10)
