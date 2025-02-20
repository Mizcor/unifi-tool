import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import unifi_tool_config

unifi_tool_config.loadSettingsFromDisk()

baseURL = unifi_tool_config.settings['base_url']
site = unifi_tool_config.settings['site']
apiURL = f"{baseURL}api/s/{site}/"
headers = {"Accept": "application/json","Content-Type": "application/json"}

session = requests.Session()

def post(endpoint,data=''):
    return session.post(apiURL+endpoint, headers = headers, json = data, verify = False, timeout = 1)

def get(endpoint,data=''):
    return session.get(apiURL+endpoint, headers = headers, json = data, verify = False, timeout = 1)

def unifi_login(username, password):
    credentials = {'username': username, 'password': password}
    login = session.post(f"{baseURL}/api/login", headers = headers, json = credentials, verify = False, timeout = 1)
    if(login.status_code != 200):
        print('Authentication error')
        return False
    else:
        print('Authenticated')
        return True

def unifi_get_devices():
    return json.loads(get('stat/device').text)['data']

def unifi_get_networks():
    return json.loads(get('rest/networkconf').text)['data']

def unifi_get_port_profiles():
    return json.loads(get('rest/portconf').text)['data']

def unifi_get_clients():
    return json.loads(get('stat/sta').text)['data']

def unifi_device_command(cmd):
    return post('cmd/devmgr', cmd)

def unifi_power_cycle_poe(mac, portidx):
    cmd = {'cmd': 'power-cycle', 'mac': mac, 'port_idx': portidx}
    return unifi_device_command(cmd)