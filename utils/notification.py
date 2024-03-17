import os 

def notification(title: str, text: str):
    os.system(f"zenity --notification --text='{title}\n{text}'")