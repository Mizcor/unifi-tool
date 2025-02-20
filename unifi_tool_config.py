import json
import tkinter as tk
from tkinter import messagebox
import common

isConfigOpen = False
configWindow = None
settings = None

defaultSettings = {
    "base_url": "https://unifi:8443/",
    "site": "default"
    }

def writeSettingsToDisk():
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=3)

def loadSettingsFromDisk():
    global settings
    with open('settings.json', 'r') as settingsFile:
        try:
            settings = json.load(settingsFile)
        except:
            settings = json.loads(json.dumps(defaultSettings))
            writeSettingsToDisk()
            messagebox.showwarning("Warning", "An error occured while loading settings, the defaults have been loaded")
