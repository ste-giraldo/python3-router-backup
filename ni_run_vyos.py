# Imports all the crucial items.
# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
import getpass
import os
import sys
import time
import cmd

#sys.tracebacklimit = 0

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H-%M")

# Gives us the information we need to connect.
def get_saved_config(host, username, password,):
    vyos = {
        'device_type': 'vyos',
        'host': host,
        'port': '21234',
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**vyos)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show conf comm")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("sh conf | grep host-name | awk {'print $2'}")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = "config_backup-" + hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gets the CSV file name, and grabs the information from it.
with open('vyos_backup_hosts.csv') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "downDevices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                get_saved_config(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2],)
