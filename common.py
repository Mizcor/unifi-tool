def setup_window(window):
    window.title("Unifi PoE tool")
    window.iconbitmap("unifi.ico")
    window.configure(borderwidth="10")
    window.tk_setPalette(background="#03244D")

def get_first_value_of_where(list, wantedKey, knownKey, knownValue):
    for item in list:
        try:
            if(str(item[knownKey])==str(knownValue)):
               return item[wantedKey]
        except:
            continue

    return None

def get_values_of_where(list,wantedKey,knownKey,knownValue):
    values = []
    for item in list:
        try:
            if(str(item[knownKey])==str(knownValue)):
               values.append(item[wantedKey])
        except:
            continue

    return values

def filter(list,wantedKey,wantedValue):
    filteredList = []
    for item in list:
        try:
            if(str(item[wantedKey]) == str(wantedValue)):
                filteredList.append(item)
        except:
            continue

    return filteredList