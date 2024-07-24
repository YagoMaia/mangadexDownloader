import os 

os.environ['DISPLAY'] = ':0'
os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'  # ou outro caminho correspondente ao seu sistema

def notification(title: str, text: str):
    os.system(f"zenity --notification --text='{title}\n{text}'")