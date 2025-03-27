import tkinter as tk
from tkinter import messagebox
from CriminalRecordApp import CriminalRecordApp
import dbs


class LoginWindow:
    def __init__(self, root):
        #///////////////////////////////////////ROOT////////////////////////////
        self.root = root
        self.root.geometry("250x100+850+400")
        self.root.title("LOGIN WINDOW")
        #///////////////////ENTRY FRAME////////////////////
        self.frameentry = tk.Frame(self.root)
        self.frameentry.grid(row=0, column=0, padx=5, pady=5)
        
        self.lbl1 = tk.Label(self.frameentry, text="User:")
        self.lbl1.grid(row=0, column=0, padx=5, pady=5)

        self.userentry = tk.Entry(self.frameentry)
        self.userentry.grid(row=0, column=1, padx=5, pady=5)
        
        self.lbl2 = tk.Label(self.frameentry, text="Password:")
        self.lbl2.grid(row=1, column=0, padx=5, pady=5)
        
        self.passentry = tk.Entry(self.frameentry, show="*", width=20)
        self.passentry.grid(row=1, column=1, padx=5, pady=5)

        self.loginbtn = tk.Button(self.frameentry, text="Login", command=self.validateLogin)
        self.loginbtn.grid(row=2, column=1, columnspan=2)
        #///////////////////ENTRY FRAME////////////////////
        
        self.output_label = tk.Label(self.root, text="", fg="red")
        self.output_label.grid(row=1, column=0)
        #///////////////////////////////////////ROOT////////////////////////////
        self.root.bind('<Return>', self.validateLogin)

    def validateLogin(self, event=None):
        print(f'Your user is: {self.userentry.get()}: and password {self.passentry.get()} ')
        if self.userentry.get() == "luther":
            if self.passentry.get() == "123":
                print('Login successful')
                self.output_label.config(text="Login Successful!", fg="green")
                messagebox.showinfo('SUCCESS LOGIN', 'TANGINAMO')
                self.open_menu_window()
            else:
                print('Wrong passs')
                self.output_label.config(text="Invalid password", fg="red")
                messagebox.showinfo('FAILED LOGIN', 'TANGINAMO MALI PASS')
        else:
            print('Login failed wrong user')
            self.output_label.config(text="Invalid username", fg="red")
            messagebox.showinfo('FAILED LOGIN', 'TANGINAMO MALI USER')

    def open_menu_window(self):
        self.root.withdraw()  
        menuroot = tk.Toplevel(self.root)
        CriminalRecordApp(menuroot)

if __name__ == "__main__":
    root = tk.Tk()
    dbs.connectDb()
    app = LoginWindow(root)
    root.mainloop()