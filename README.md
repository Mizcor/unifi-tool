# UniFi Tool
This tool is meant to help with operations that are otherwise difficult or tedious to perform in the Network Application.

The only current feature is the ability to PoE power cycle all clients on a network by VLAN ID or cycle a client by its IP or MAC address.

# Notes
This has only been tested on HostiFi

No additional dependencies are needed other than Python 3

When installed just run unifi-tool.py to start the application

Before running the application for the first time, check in settings.json that the base URL is pointing to your UniFi controller