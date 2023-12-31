# Python Script for Network Automation

## A Brief Summary
This script can be used for generating output of some commands or even for configuring network devices. 

As on Dec-23, it can be used only for Cisco Devices.

## Features
Automatically decides whether it requires to generate output or to configure any network devices

Summary of the actions will be shown on command line

Automatically captures the snap of the required section before and after configuration and saves it in a unique filed stored in directory 'log'.

A file named 'log' will be generated each time the scripts run which will contains all the actions performed on the devices


# prerequisite
netmiko module must be present


## How to Run

Add Credential to cred.py
```commandline
username = 'cisco' #username
password = 'cisco' #password
secret = 'cisco' #enable password
```

Add the list of devices in device-list.txt . Each entry in a separate line
```commandline
x.x.x.x
y.y.y.y
z.z.z.z
```

Add the command for which output is needed to 'verification' file. The same command can be used to verify the configuration before and after making the changes
e.g. To see list of users added on the device
```commandline
sh ip int br | i Loo
```

add the command for configuration
```commandline
int loo 0
ip add 1.1.1.1 255.255.255.255
no shut
```


Run Main.py

<br><br>
#### Features to be added later
Automatic backup before making any changes
<br>
Saving configuration after making changes
<br>
Take the input of credentials on the go instead of saving it in the file
<br>
Read data from excel which contains, unique credential for each device and then run specific command mentioned in the column for that specific device
<br>
More to be added...
