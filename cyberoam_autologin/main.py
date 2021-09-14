from PIL import Image, ImageDraw
from pystray import MenuItem as item
import pystray
import requests
import threading
import sys
import os
import time


# edit these values please
username = "USERNAME"
password = "PASSWORD"
gateway = "GATEWAY"
port = "PORT"
url = "http://{}:{}/httpclient.html".format(gateway, port)

session = requests.Session()

global logged_in
logged_in = False

def create_image() -> Image:
    # Create an icon to display on system tray
    width = 100
    color1, color2 = "black", (235,0,235)
    height = 100
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


def notify(title: str, msg: str):
    # make a system notification, it'll only work on linux.
    os.system(f"notify-send '{title}' '{msg}'")


def login():
    global logged_in
    
    try:
        data_login = {'mode': 191, 'username': username, 'password': password, 'btnSubmit': 'Login'}
        r = session.post(url, data=data_login)
    except Exception as error:
        notify("Error during login.", error)
        logged_in = False
    else:
        
       # if we didnt get any exception:
        if  not logged_in:
            notify("Logged in.", "Successfully logged in.")
        logged_in = True

        t = threading.Timer(600.0, login)
        t.setDaemon(True)
        t.start()


def logout():
    global logged_in

    if not logged_in:
        notify("Already logged out", "")
        return

    try:
        data = {'mode': 193, 'username': username, 'password': password, 'btnSubmit': 'Logout'}
        r = session.post(url, data=data)
    except Exception:
        notify("Error during logout.", "Logout via webclient.")

    else:
        notify("Logged Out.", "Successfully logged out.")
        logged_in = False
     

def quit():
    sys.exit()


def system_tray():
    # build the system tray functions
    menu = (
        item("Log in", login),
        item("Log out", logout),
        item("Quit", quit)
    )

    icon = pystray.Icon("iconname", create_image(), "Cyberroam Autologin", menu)

    icon.run()


def main():
    login()
    system_tray()
    

if __name__ == "__main__":
    main()
