import tkinter as tk
import random
import dbs
from tkinter import messagebox
import sqlite3

def addRecord():
    add_window = tk.Toplevel()
    add_window.title("Add Record")
    add_window.geometry("800x400+550+200")
    
    title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
    title_label.place(relx=0.38, y=20)
    
    def addCrimeRecord():
        add_window.destroy()
        adCrime = tk.Toplevel()
        adCrime.title("Add New Crime Record")
        adCrime.geometry("800x800+550+100")
        
        # Get the next crime ID
        conn = sqlite3.connect("criminal_records.db")
        cur = conn.cursor()
        cur.execute("SELECT MAX(crime_Id) FROM crimes")
        last_crime_id = cur.fetchone()[0]
        next_crime_id = last_crime_id + 1 if last_crime_id else 1
        conn.close()
        
        title_label = tk.Label(adCrime, text="ADD NEW CRIME RECORD", font=("Arial", 20, "bold"))
        title_label.place(relx=0.30, y=20)
        
        frame = tk.Frame(adCrime)
        frame.place(relx=0.23, y=100)
        
        tk.Label(frame, text="Crime ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=20, sticky="e")
        tk.Label(frame, text=next_crime_id, font=("Arial", 14, "bold")).grid(row=0, column=1, padx=20, pady=3)
        
        tk.Label(frame, text="Crime Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=20, sticky="e")
        crime_name_entry = tk.Entry(frame, width=30, bd=3)
        crime_name_entry.grid(row=1, column=1, padx=2, pady=10)

        tk.Label(frame, text="Crime Sentence: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=20, sticky="e")
        crime_sentence_entry = tk.Entry(frame, width=30, bd=3)
        crime_sentence_entry.grid(row=2, column=1, padx=2, pady=10)

        def confirm_add():
            crime_name = crime_name_entry.get().strip()
            crime_sentence = crime_sentence_entry.get().strip()

            if not crime_name or not crime_sentence:
                messagebox.showerror("Error", "Crime Name and Crime Sentence cannot be empty!")
                return

            confirm_window = tk.Toplevel()
            confirm_window.title("Confirm Add Crime Record")
            confirm_window.geometry("500x500+600+350")
            
            tk.Label(confirm_window, text="CONFIRM ADD CRIME RECORD", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=20)
            
            tk.Label(confirm_window, text="Crime ID:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
            tk.Label(confirm_window, text=next_crime_id, font=("Arial", 14, "bold")).grid(row=1, column=1, padx=20, pady=3)
            
            tk.Label(confirm_window, text="Crime Name:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
            tk.Label(confirm_window, text=crime_name, font=("Arial", 14, "bold")).grid(row=2, column=1, padx=20, pady=3)
            
            tk.Label(confirm_window, text="Crime Sentence:", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="e")
            tk.Label(confirm_window, text=crime_sentence, font=("Arial", 14, "bold")).grid(row=3, column=1, padx=20, pady=3)
            
            tk.Label(confirm_window, text="Are you sure you want to add this record?", font=("Arial", 14, "bold")).grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="e")
            
            def add_to_db():
                dbs.add_crime_record(next_crime_id, crime_name, crime_sentence)
                messagebox.showinfo("Success", "New crime record added successfully!")
                confirm_window.destroy()
                adCrime.destroy()
            
            yes = tk.Button(confirm_window, text="Yes", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=add_to_db)
            yes.grid(row=5, column=0, padx=5, pady=10)
                
            no = tk.Button(confirm_window, text="No", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=confirm_window.destroy)
            no.grid(row=5, column=1, padx=5, pady=10)

        tk.Button(frame, text="Submit", width=15, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=confirm_add).grid(row=4, column=1, padx=0, pady=20)
        

        
    def addCriminalRecord():
        pass
    
    
    addCrime = tk.Button(add_window, text="Add Crime Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=addCrimeRecord)
    addCrime.place(x=250, y=100)
    
    addCriminal = tk.Button(add_window, text="Add Criminal Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
    addCriminal.place(x=250, y=200)
   
   

def deleteRecord():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Record")
    delete_window.geometry("800x400+550+200")

    title_label = tk.Label(delete_window, text="DELETE RECORD", font=("Arial", 20, "bold"))
    title_label.place(relx=0.37, y=20)
    ###############################################
    def delCrimeRecord():
        pass
    
    def delCriminalRecord():
        delete_window.destroy()
        delCriminal = tk.Toplevel()
        delCriminal.title("Delete Criminal Record")
        delCriminal.geometry("800x800+550+100")
        
        title_label = tk.Label(delCriminal, text="DELETE CRIMINAL RECORD", font=("Arial", 20, "bold"))
        title_label.pack(padx=10, pady=20)
        
        frame = tk.Frame(delCriminal)
        frame.place(relx=0.20, y=80)
        
        frame2 = tk.Frame(delCriminal)
        frame2.place(relx=0.20, y=200)
        
        tk.Label(frame, text="Enter Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        criminal_id = tk.Entry(frame, width=30, bd=3)
        criminal_id.grid(row=0, column=1, padx=2, pady=10)
        ###############################################
        def showRecord(id):
            frame2.place(relx=0.20, y=200)
            search_result = dbs.search(id)
            if search_result:
                criminalId = search_result[0]
                name = search_result[1]
                crime = search_result[2]
                location = search_result[3]
                date = search_result[4]
                
                tk.Label(frame2, text="Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
                tk.Label(frame2, text=criminalId, font=("Arial", 14, "bold"), width=30).grid(row=0, column=1, padx=10, pady=3)
                
                tk.Label(frame2, text="Name: ", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="e")
                tk.Label(frame2, text=name, font=("Arial", 14, "bold"), width=30).grid(row=1, column=1, padx=10, pady=3)
                
                tk.Label(frame2, text="Crime: ", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="e")
                tk.Label(frame2, text=crime, font=("Arial", 14, "bold"), width=30).grid(row=2, column=1, padx=10, pady=3)
                
                tk.Label(frame2, text="Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="e")
                tk.Label(frame2, text=location, font=("Arial", 14, "bold"), width=30).grid(row=3, column=1, padx=10, pady=3)
                
                tk.Label(frame2, text="Date: ", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="e")
                tk.Label(frame2, text=date, font=("Arial", 14, "bold"), width=30).grid(row=4, column=1, padx=10, pady=3)
                
                tk.Label(frame2, text="Are you sure you want to delete this record?", font=("Arial", 14, "bold")).grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="e")
                yes = tk.Button(frame2, text="Yes", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: confirm_delete(criminalId))
                yes.grid(row=6, column=0, padx=5, pady=10)
                
                no = tk.Button(frame2, text="No", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: frame2.place_forget())
                no.grid(row=6, column=1, padx=5, pady=10)
            else:
                messagebox.showerror("Error", "Record not found in database!", parent=delCriminal)
        ###############################################
        def confirm_delete(criminalId):
            if dbs.delete_criminal_record(criminalId):
                messagebox.showinfo("Success", "Record deleted successfully!")
                for widget in frame2.winfo_children():
                    widget.destroy()
                delCriminal.destroy()
            else:
                messagebox.showerror("Error", "Failed to delete the record!")
        ###############################################
        enter = tk.Button(frame, text="Enter", width=5, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=lambda: showRecord(criminal_id.get().strip()))    
        enter.grid(row=0, column=3, columnspan=2, padx=20)
    ###############################################
    deleteCrime = tk.Button(delete_window, text="Delete Crime Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
    deleteCrime.place(x=250, y=100)
    
    deleteCriminal = tk.Button(delete_window, text="Delete Criminal Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delCriminalRecord)
    deleteCriminal.place(x=250, y=200)
        
        
dbs.connectDb()
dbs.add_crimes()

root = tk.Tk()

root.title("Crime Record Management")
root.geometry("800x600+550+100")

label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
label.pack(padx=10, pady=20)

#Add Record
add = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=addRecord)
add.pack(padx=20, pady=20)

#Edit Record
edit = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
edit.pack(padx=20, pady=20)

#Delete Record
delete = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=deleteRecord)
delete.pack(padx=20, pady=20)

#View Records
logout = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
logout.pack(padx=20, pady=20)

root.mainloop()