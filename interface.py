import tkinter as tk

root = tk.Tk()
root.title("Interface")
root.geometry("800x400+600+50")

label = tk.Label(root, text="CRIME RECORD MANAGEMENT", font=("Arial", 20, "bold"))
label.pack(padx=10, pady=20)
add = tk.Button(root, text="Add Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
add.pack(padx=20, pady=20)
edit = tk.Button(root, text="Edit Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
edit.pack(padx=20, pady=20)
delete = tk.Button(root, text="Delete Record", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
delete.pack(padx=20, pady=20)
logout = tk.Button(root, text="Logout", width=30, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black")
logout.pack(padx=20, pady=20)

root.mainloop()