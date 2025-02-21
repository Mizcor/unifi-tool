# UniFi Tool
This tool is meant to help with operations that are otherwise difficult or tedious to perform in the Network Application.

![GuI Demo](/images/app.png)
### Current Features:
* PoE Operations:
  * PoE power cycle clients by VLAN ID
  * PoE power cycle client by IP or MAC address
* Export entire device configs to JSON

### Notes
This has only been tested on HostiFi

No additional dependencies are needed other than Python 3

When installed just run unifi-tool.py to start the application

Before running the application for the first time, check in settings.json that the base URL is pointing to your UniFi controller