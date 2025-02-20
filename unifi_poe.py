import tkinter as tk
import unifi_api
from tkinter import messagebox
import ipaddress
import re
import common

isPoeToolOpen = False
poeWindow = None
poeEntry = None

def onClose():
    global isPoeToolOpen
    isPoeToolOpen = False
    poeWindow.destroy()

def cycleDevicesWithList(list):
    portCount = 0
    errorCount = 0

    for mac in list:

        portList = list.get(mac)

        for port in portList:
            if(unifi_api.unifi_power_cycle_poe(mac, port).status_code == 200):
                portCount += 1
            else:
                errorCount += 1
    if(errorCount == 0):
        messagebox.showinfo("info", f"Reset {portCount} port(s)")
    else:
        messagebox.showinfo("info", f"Reset {portCount} port(s)\n{errorCount} ports could not be reset")

def cycleByVlan(vlanID):
    networks = unifi_api.unifi_get_networks()
    nativeNetworkID = common.get_first_value_of_where(networks, '_id', 'vlan', vlanID)

    if(nativeNetworkID == None):
        messagebox.showerror("Error", f"Invalid VLAN ID: {vlanID}")
        return

    portProfiles = unifi_api.unifi_get_port_profiles()
    portProfileID = common.get_first_value_of_where(portProfiles,'_id','native_networkconf_id', nativeNetworkID)

    print ('native vlan id:' + str(nativeNetworkID))
    print ('native port config id:' + str(portProfileID))

    devices = unifi_api.unifi_get_devices()
    resetList = dict()

    for device in devices:
        mac = device['mac']
        resetList[mac]=[]

        try:
            portlist = common.get_values_of_where(device['port_table'], 'port_idx', 'native_networkconf_id', nativeNetworkID)
            portlist.extend(common.get_values_of_where(device['port_table'], 'port_idx', 'portconf_id', portProfileID))

            resetList[mac] = portlist
        except:
            continue
    
    cycleDevicesWithList(resetList)

def cycleClient(client):
    if(str(client['is_wired'])=='False'):
        messagebox.showerror("Error", "This client is wireless")
        return
    
    switchMac = client['sw_mac']
    switchPort = client['sw_port']

    unifi_api.unifi_power_cycle_poe(switchMac, switchPort)
    messagebox.showinfo("info", "Device has been power cycled")

def cycleByMACAddress(mac):
    clients = unifi_api.unifi_get_clients()
    client = common.filter_down(clients, 'mac', mac)

    if(len(client) == 0):
        messagebox.showerror("Error", "Client not found")
        return

    cycleClient(client[0])

def cycleByIPAddress(ip):
    clients = unifi_api.unifi_get_clients()
    client = common.filter(clients, 'ip', ip)

    if(len(client) == 0):
        messagebox.showerror("Error", "Client not found")
        return
    
    cycleClient(client[0])

def cyclePoe():
    if(len(poeEntry.get()) == 0):
        messagebox.showerror("Error", "Please enter a valid VLAN ID or client IP/MAC")
        return
    
    try:
        ipaddress.ip_address(poeEntry.get())
        cycleByIPAddress(poeEntry.get())
        return
    except ValueError:
        pass

    macRegex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    if(macRegex.match(poeEntry.get())):
        cycleByMACAddress(poeEntry.get())
        return
    
    if(poeEntry.get().isnumeric()):
        cycleByVlan(poeEntry.get())
        return
    
    messagebox.showerror("Error", "Please enter a valid VLAN ID or client IP/MAC")

def showWindow():
    global isPoeToolOpen
    global poeWindow
    global poeEntry

    if(isPoeToolOpen):
        return
    
    isPoeToolOpen = True

    poeWindow = tk.Tk()
    common.setup_window(poeWindow)
    poeWindow.protocol("WM_DELETE_WINDOW", onClose)

    entryLabel = tk.Label(poeWindow, text="VLAN ID (all clients) or client IP/MAC")
    entryLabel.pack()
    poeEntry = tk.Entry(poeWindow)
    poeEntry.pack()
    cycleButton = tk.Button(poeWindow, text="Power cycle", command=cyclePoe)
    cycleButton.pack()

    poeWindow.mainloop()