import tkinter as tk
import unifi_api as unifi
from tkinter import messagebox
import common
import unifi_tool_config

isLoggedIn = False

loginWindow = None
usernamebox = None
passwordbox = None

def handle_login_button():
    global isLoggedIn

    if(len(usernamebox.get()) == 0 or len(passwordbox.get()) == 0):
        messagebox.showerror("Error", "Missing username or password")
        return
    
    isLoggedIn = unifi.unifi_login(usernamebox.get(), passwordbox.get())

    if(isLoggedIn):
        loginWindow.destroy()
    else:
        messagebox.showerror("Error", "Login failed")

def show_legal_info():
    messagebox.showinfo("legal", """This software is not affiliated with, endorsed by, or associated with Ubiquiti Inc. or its product UniFi. Ubiquiti Inc. and UniFi are trademarks of Ubiquiti Inc. and all rights to such marks are owned by Ubiquiti Inc. Any use of the names, logos, or trademarks is for identification purposes only and does not imply any official connection or endorsement.

This software is a tool designed for use with computer networks. While it aims to assist in managing your network, the developers are not responsible for any damages, losses, or issues arising from the use of this software. By using this software, you acknowledge that you do so at your own risk, and agree that the developers are not liable for any direct, indirect, incidental, or consequential damages, including but not limited to loss of data, service interruptions, or network malfunctions.""")

def showWindow():
    global loginWindow
    global usernamebox
    global passwordbox

    loginWindow = common.create_window('Unifi Login')
    loginWindow.grid_columnconfigure((0,1), weight=1)

    usernamebox = tk.Entry(loginWindow)
    passwordbox = tk.Entry(loginWindow, show="*")

    label1 = tk.Label(loginWindow, text="Username")
    label2 = tk.Label(loginWindow, text="Password")

    label1.grid(row=1, column=0)
    usernamebox.grid(row=1, column=1)

    label2.grid(row=2, column=0)
    passwordbox.grid(row=2, column=1)

    button = tk.Button(loginWindow, command=handle_login_button, text="Login", )
    button.grid(row=3,column=0, columnspan=2)

    button = tk.Button(loginWindow, command=show_legal_info, text="Legal Disclaimer", )
    button.grid(row=4,column=0, columnspan=2)

    loginWindow.mainloop()