import os
import time
from datetime import datetime
import subprocess


def notify(title, message):
    print(subprocess.run(["notify-send", title, message]))

def rclone(source, destination, protocol): # add a logging module
    print(subprocess.run([
        "rclone", 
        "-P", # Show progress during transfer
        protocol, 
        source, 
        destination
    ]))


