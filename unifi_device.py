import tkinter as tk
import common
import unifi_api
import json
import unifi_tool_config
import os
import re

devices = None
deviceInfoBox = None
exportSelectedButton = None
selectedDeviceIndex = -1

def exportAll():
    filename = f'{unifi_tool_config.settings['export_path']}/devices.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        file.write(json.dumps(devices, indent=3))

    for index in range(len(devices)):
        exportSelected(index)
        
def exportSelected(selected=-1):

    index = selected
    if (selected == -1):
        index = selectedDeviceIndex

    device = devices[index]
    cleaned_filename = re.sub(r'[^a-zA-Z0-9\s-]', '', device.get('name'))
    cleaned_filename = cleaned_filename.replace(' ', '_')

    filePath = f'{unifi_tool_config.settings['export_path']}/{cleaned_filename}.json'

    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    with open(filePath, 'w') as file:
        file.write(json.dumps(device, indent=3))

def listField(fieldname, device):
    deviceInfoBox.insert('end', f"{fieldname}: {device.get(fieldname)}\n")
    exportSelectedButton.config(state='normal')

def showDeviceInfo(deviceIndex):
    device = devices[deviceIndex]
    deviceInfoBox.config(state='normal')
    deviceInfoBox.delete('1.0', 'end')
    listField('name', device)
    listField('ip', device)
    listField('mac', device)
    deviceInfoBox.config(state='disabled')

def onDeviceSelect(event):
    global selectedDeviceIndex
    selectedDeviceIndex = event.widget.curselection()[0]
    showDeviceInfo(event.widget.curselection()[0])

def showWindow():
    global devices
    global deviceInfoBox
    global exportSelectedButton
    deviceWindow = common.create_window('UniFi Devices')

    listbox = tk.Listbox(deviceWindow, selectmode='browse')
    scrollbar = tk.Scrollbar(deviceWindow)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    listbox.pack(side='left', fill='both')
    scrollbar.pack(side='right', fill='y')

    devices = unifi_api.unifi_get_devices()
    
    for device in devices:
        listbox.insert(tk.END, device.get('name'))

    listbox.config(yscrollcommand = scrollbar.set)
    listbox.bind('<<ListboxSelect>>', onDeviceSelect)
    scrollbar.config(command = listbox.yview)

    exportAllButton = tk.Button(deviceWindow, text='Export all', command=exportAll)
    exportAllButton.pack()
    
    exportSelectedButton = tk.Button(deviceWindow, text='Export selected', state='disabled', command=exportSelected)
    exportSelectedButton.pack()

    deviceInfoBox = tk.Text(deviceWindow, state='disabled')
    deviceInfoBox.pack()

    deviceWindow.mainloop()