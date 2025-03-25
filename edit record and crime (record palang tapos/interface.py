import tkinter as tk
import random
import dbs
from tkinter import messagebox


def addRecord():
    add_window = tk.Toplevel()
    add_window.title("Add Record")
    add_window.geometry("800x400+600+50")
    
    title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
    title_label.place(relx=0.38, y=20)
    
    frame = tk.Frame(add_window)
    frame.place(relx=0.20, y=80)
    
    randNum = random.randint(10000, 99999)
    
    #ID
    tk.Label(frame, text="Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    criminalId = tk.Label(frame, text=randNum, font=("Arial", 14, "bold"), width=30).grid(row=0, column=1, padx=10, pady=3)
    
    #Name
    tk.Label(frame, text="Enter Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    criminalName = tk.Entry(frame, width=30, bd=3)
    criminalName.grid(row=1, column=1, padx=2, pady=10)
    
    #Crime
    crime_var = tk.StringVar()
    crime_var.set("Felony")
    tk.Label(frame, text="Choose Crime: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
    crime_options = ["Felony", "Misdemeanor", "Theft", "Assault", "Fraud"]
    crime_dropdown = tk.OptionMenu(frame, crime_var, *crime_options)
    crime_dropdown.grid(row=2, column=1, padx=5, pady=10)
    crime_dropdown.config(width=24, bd=3)
    
    #Location
    tk.Label(frame, text="Enter Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="e")
    criminalLocation = tk.Entry(frame, width=30, bd=3)
    criminalLocation.grid(row=3, column=1, padx=2, pady=10)
    
    #Date
    tk.Label(frame, text="Enter Date(YEAR): ", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="e")
    recordDate = tk.Entry(frame, width=30, bd=3)
    recordDate.grid(row=4, column=1, padx=2, pady=10)
    
    def add_to_db():
        name = criminalName.get().strip()
        crime = crime_var.get().strip()
        location = criminalLocation.get().strip()
        date = recordDate.get().strip()
        
        if name == "" or location == "" or date == "":
            messagebox.showerror("Error", "Name, Location and Date cannot be empty!")
            return
        
        dbs.add_record(randNum, name, crime, location, date)
        messagebox.showinfo("Succes", "Record added successfully!")
        add_window.destroy()

    submit = tk.Button(add_window, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
    submit.place(relx=0.4, y=350)

dbs.connectDb()


root = tk.Tk()
root.title("Interface")
root.geometry("800x400+600+50")




def editRecord():
    edit_window = tk.Toplevel()
    edit_window.title("Edit Record")
    edit_window.geometry("900x900+450+40")
    edit_title = tk.Label(edit_window, text="EDIT RECORD", font=("Arial", 20, "bold"))
    edit_title.place(relx=0.35, y=20)
    
    frame = tk.Frame(edit_window)
    frame.place(relx=0.20, y=80)
    tk.Label(frame, text="Enter Criminal ID to edit: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    criminalId = tk.Entry(frame, width=30, bd=3)
    criminalId.grid(row=1, column=1, padx=250, pady=10)

    def checkId():
        crimId = criminalId.get().strip()

        if not crimId.isdigit():    #checker if valid input(numbers only)

            messagebox.showerror("Wrong input!", "Enter a number only.")
            edit_window.focus_force() #napupunta sa likod ng main menu yung editwindow pag wala to
        
        else:
         crimId = int(crimId)

         if not dbs.checkExist(crimId): #checks if inputted ID is on the database
             messagebox.showerror("Criminal not found", "Criminal does not exist.")
             edit_window.focus_force() #napupunta sa likod ng main menu yung editwindow pag wala to
         else:
             criminalId.config(state="readonly")
             submit.destroy()
             crimData = dbs.getCriminalData(crimId)
           #Name update
        

             tk.Label(frame, text=f"Name: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")
             criminalName = tk.Entry(frame, width=30, bd=3)
             criminalName.grid(row=3, column=1, padx=250, pady=10)
             criminalName.insert(0, crimData["name"])

                    #Crime
             crime_var = tk.StringVar()
             crime_var.set(crimData["crime"])
             tk.Label(frame, text="Crime: ", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")
             crime_options = ["Felony", "Misdemeanor", "Theft", "Assault", "Fraud"]
             crime_dropdown = tk.OptionMenu(frame, crime_var, *crime_options)
             crime_dropdown.grid(row=5, column=1, padx=250, pady=10)
             crime_dropdown.config(width=24, bd=3)
            

             #Location
             tk.Label(frame, text="Location: ", font=("Arial", 14, "bold")).grid(row=7, column=0, padx=10, pady=10, sticky="w")
             criminalLocation = tk.Entry(frame, width=30, bd=3)
             criminalLocation.grid(row=7, column=1, padx=2, pady=10)
             criminalLocation.insert(0, crimData["location"])


             #Date
             tk.Label(frame, text="Year of Arrest: ", font=("Arial", 14, "bold")).grid(row=9, column=0, padx=10, pady=10, sticky="w")
             recordDate = tk.Entry(frame, width=30, bd=3)
             recordDate.grid(row=9,column=1, padx =2, pady=10)
             recordDate.insert(0, crimData["date"])

             
             def submitEdit():
                crimName = criminalName.get().strip()
                crimDesc = crime_var.get().strip()
                crimeLoc = criminalLocation.get().strip()
                crimeDate = recordDate.get().strip()
                if (messagebox.askokcancel(title="Confirm update", message="Are you sure you want to update the record?")): 
                    
                    dbs.editRecord(crimId, crimName, crimDesc, crimeLoc, crimeDate)
                    messagebox.showinfo(title="Update Success!", message="Successfully updated the record!")
                else:
                    edit_window.focus_force()
             


             update = tk.Button(frame, text="Update Record", font=("Arial", 10, "bold"), command=submitEdit)
             update.grid(row=10, column=0, columnspan=2, pady=10, sticky="nw")


    submit = tk.Button(edit_window, text="Submit", width=15, bd=3, font=("Arial", 12), command=checkId)
    submit.place(relx = 0.35, y=200)







label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
label.pack(padx=10, pady=20)
add = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=addRecord)
add.pack(padx=20, pady=20)
edit = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=editRecord)
edit.pack(padx=20, pady=20)
delete = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
delete.pack(padx=20, pady=20)
logout = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
logout.pack(padx=20, pady=20)

root.mainloop()