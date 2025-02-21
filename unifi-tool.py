import unifi_login
import unifi_poe
import unifi_device
import tkinter as tk
import common

toolWindow = None

def showWindow():
    toolWindow = common.create_window('UniFi Tools')

    button = tk.Button(toolWindow, text="PoE power cycle tool", command=unifi_poe.showWindow)
    button.pack()
    button = tk.Button(toolWindow, text="Devices", command=unifi_device.showWindow)
    button.pack()

    toolWindow.mainloop()

def main():
    unifi_login.showWindow()
    if(unifi_login.isLoggedIn):
        showWindow()

if __name__ == "__main__":
    main()