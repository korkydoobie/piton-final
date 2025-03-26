import tkinter as tk
import random
import dbs
from tkinter import messagebox
import sqlite3

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

        def submitEdit():
            name = criminalName.get().strip()
            if messagebox.askyesno("Confirm Addition of Criminal", f"Do you wish to add {name} in the criminal list?"):
                dbs.addCriminal(name)
                messagebox.showinfo("Criminal Addition Success", f"{name} was added to the criminal list.")
                criminal_window.destroy()
            

        criminalAdd = tk.Button(frame, text="Add Criminal", font=("Arial", 10, "bold"), command=submitEdit)
        criminalAdd.grid(row=10, column=1, padx=10,columnspan=2, pady=10, sticky="nw")


###RONNSHITS##############
    def delete_criminal_record(self):
        if dbs.checkEmpty("criminals"):
            messagebox.showerror("Missing Data", "No Criminals to Delete. Please add records first.")
        elif not dbs.get_criminals_not_in_records():
            messagebox.showerror("No Available Records", "No Available Criminals to Delete.")
        else:
            delCriminal = tk.Toplevel(self.root)
            delCriminal.title("Delete Criminal Record")
            delCriminal.geometry("800x800+550+100")

            title_label = tk.Label(delCriminal, text="DELETE CRIMINAL RECORD", font=("Arial", 20, "bold"))
            title_label.pack(padx=10, pady=20)

            frame = tk.Frame(delCriminal)
            frame.place(relx=0.20, y=80)
            
            criminal_var = tk.StringVar()
            criminal_var.set("Select Criminal")  # Default value
            criminals_list = dbs.get_criminals_not_in_records()
            
            tk.Label(frame, text="Criminal:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
            criminal_dropdown = tk.OptionMenu(frame, criminal_var, *[f"{id} - {name}" for id, name in criminals_list])
            criminal_dropdown.grid(row=1, column=1, padx=10, pady=10)
            criminal_dropdown.config(width=30, bd=3)
            
            def delete():
                criminal_id = criminal_var.get().strip(" - ")[0]
                if criminal_id == "Select Criminal":
                    messagebox.showerror("Error", "Please select a criminal to delete!")
                    return
                else:
                    dbs.deleteCriminal(criminal_id)
                    messagebox.showinfo("Success", "Criminal record deleted successfully!")
                    delCriminal.destroy()

            
            submit = tk.Button(frame, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black" ,command=delete)
            submit.grid(row=2, column=1, padx=2, pady=10)

