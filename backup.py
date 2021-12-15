# python 3.9
import os
import time
from datetime import datetime
import subprocess

# TODO(osman) add backup logging



os.chdir("/home/osman")
os.system("notify-send Backup started")

assert os.name == "posix"  # only works on linux

user = "osman"
home_folder = "/home/osman"

# Remotes
onedrive = "onedrive_remote:"
onedrivebackup = onedrive + "Backups"
onedriveuser = onedrive + user
onedrivefiles = onedrive + "Files"

googleDrives = [] # TODO(osman) add later

# Locals
workplaceFolder = f"{home_folder}/Workplace"  # daily backup and daily sync to onedrive and google drives
filesFolder     = f"{home_folder}/Files"      # Constant sync, for bedir and osman
filesFolder     = f"{home_folder}/Files"      # Constant sync, for bedir and osman


def get_date():
    # HH:MM_DD-MM-YYYY
    today = datetime.now()
    return today.strftime("%H-%M_%d-%m-%Y")


def workplace_backup(source=workplaceFolder, destination=onedrivebackup, protocol="copy", delete_after=True):
    # for some reason these shell commands doesnt work with subprocess module
    filename = f"{user}_backup_{get_date()}.tar.gz"

    print(os.system(f"tar --force-local -zcvf {filename} {source.split('/')[-1]}"))      # Compress the onedrive folder
    print(os.system(f"rclone -P {protocol} {filename} {destination}"))                   # upload it

    if delete_after:
        print(os.system(f"rm {home_folder}/*.gz")) 


def notify(title, message):
    print(subprocess.run(["notify-send", title, message]))


def sync(source=workplaceFolder, destination=onedriveuser, protocol="sync"):
    print(subprocess.run(["rclone", "-P", protocol, source, destination]))


def main():
    beginning = time.time()

    workplace_backup() # A

    sync(source=workplaceFolder, destination=onedriveuser)
    sync(source=onedrivefiles, destination=filesFolder, protocol="copy")
    sync(source=filesFolder, destination=onedrivefiles)

    for remotes in googleDrives:
        sync(source=workplaceFolder, destination=remotes)

    uptime = round(time.time() - beginning)
    minutes, seconds = divmod(uptime, 60)
    notify("Backup sequence is complete", f"Uptime: {minutes} minute {seconds} second")


if __name__ == "__main__":
    main()
