import os
from netmiko import ConnectHandler
import time
import cred
import datetime

def writeLog(ip,hostname,verification_cmd,logfilep,output):
    logfilep.write(f'Device: {hostname}, IP: {ip}, Command Executed: {verification_cmd}')
    logfilep.write('\n')
    logfilep.write(output)
    logfilep.write('\n')
    logfilep.write('--' * 40)
    logfilep.write('\n')
#closed writelog()
def verification(connection,verification_cmd):
    output = connection.send_command(verification_cmd)
    return output
#closed verification()
def config(connection,config_cmd,logfilep):
    logfilep.write('Configuring...:\n')
    config_output = connection.send_config_set(config_cmd)
    logfilep.write(config_output)
    logfilep.write('\n')
    logfilep.write('--' * 40)
    print(config_output)
#closed config()
def connect(ip,username,password,enable):
    cisco_device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
        'port': '22',  # optional, default 22
        'secret': enable,  # optional,enable pwd, default ''
        'verbose': True  # optional, default False
    }
    # Connecting to device
    connection = ConnectHandler(**cisco_device)
    connection.enable()
    return connection
#closing connect

#MAIN starting from here
#creating logfiles and its pointer
now = datetime.datetime.now()
logfilename = f'log-{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'
logfilep = open(f'logs/{logfilename}','w')
#reading verification command
with open('verification', 'r') as r:
    verification_cmd = r.read()
#reading list of devices
with open('device-list.txt', 'r') as f:
    devices = f.read().splitlines()
#checking if configuration required
print('Checking if Configuration command available...')
isConfigRequired = os.stat('config').st_size!=0
if(isConfigRequired):
    with open('config','r') as conf:
        config_cmd = conf.read()
    print('Below Configuration command found:')
    print('**'*50)
    print(config_cmd)
    print('**'*50)
    print('Configuration will start in 3 seconds.')
    print('Exit and make the changes if above command is not to be configured.')
    #time.sleep(3)
    print('\nStarting the Configuration now...\n')
    # connecting devices individually
    for ip in devices:
        connection = connect(ip, cred.username, cred.password, cred.secret)
        hostname = connection.find_prompt()[:-1]
        output = verification(connection, verification_cmd)
        # writing output to logfile before making changes
        logfilep.write('Before:\n')
        writeLog(ip, hostname, verification_cmd, logfilep, output)
        #configuring
        connection = connect(ip, cred.username, cred.password, cred.secret)
        config(connection,config_cmd,logfilep)
        # writing output to logfile after making changes
        logfilep.write('\nAfter:\n')
        output = verification(connection, verification_cmd)
        writeLog(ip, hostname, verification_cmd, logfilep, output)
        logfilep.write('##'*40)
        logfilep.write('\n')
        connection.disconnect()
        print(f'Closed Connection to {ip}')
else:
    print('No config command found.')
    print(f'Running "{verification_cmd}" on All the devices.')
    for ip in devices:
        connection = connect(ip, cred.username, cred.password, cred.secret)
        hostname = connection.find_prompt()[:-1]
        output = verification(connection,verification_cmd)
        #writing to logfile
        writeLog(ip,hostname,verification_cmd,logfilep,output)
        print(f'Closed Connection to {ip}')
logfilep.close()