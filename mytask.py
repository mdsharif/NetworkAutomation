from netmiko import ConnectHandler
import time
import cred

import threading
start = time.time()
def task(device,verification,config_file,logfilep):
    #Connecting to device
    connection = ConnectHandler(**device)
    connection.enable()
    #Verifying before making changes
    print(f'{verification} on {device['host']}')
    # writing to log file before changes
    logfilep.write(f'Before : {device['host']}-->\t{verification}\n')
    output = connection.send_command(verification)
    print(output)
    logfilep.write(output)
    logfilep.write('\n')
    logfilep.write('-'* 60)
    logfilep.write('\n')
    #changing configuration
    logfilep.write(f'Configuring from file : {config_file}\n')
    config_output = connection.send_config_from_file(config_file)
    print(config_output)
    logfilep.write(config_output)
    logfilep.write('\n')
    logfilep.write('-' * 60)
    logfilep.write('\n')
    #verifying after changing configuration
    logfilep.write(f'After : {device['host']}-->\t{verification}\n')
    output = connection.send_command(verification)
    print(output)
    logfilep.write(output)
    logfilep.write('\n')
    #completed
    logfilep.write('#' * 60)
    logfilep.write('\n')
    print('closing connection')
    connection.disconnect()
    print(f'Closed Connection to {device['host']}')
    print('#' * 40)

##########main###########3
with open('device-list.txt', 'r') as f:
    devices = f.read().splitlines()
# device_list = list()
# threads = list()
#creating log file and its pointer
from datetime import datetime
now = datetime.now()
logfilename = f'log-{now.year}{now.month}{now.day}-{now.hour}{now.minute}{now.second}'
f = open(f'logs/{logfilename}','w')
print('log file name '+logfilename)
for ip in devices:
    cisco_device = {
        'device_type':'cisco_ios',
        'host' : ip,
        'username': cred.username,
        'password': cred.password,
        'port': '22',       #optional, default 22
        'secret': cred.secret,  #optional,enable pwd, default ''
        'verbose': True     #optional, default False
    }
    with open('verification','r') as r:
        verification = r.read()
    task(cisco_device, verification,'config',f)

f.close()
    # th = threading.Thread(target=backup,args=(cisco_device,))
    # threads.append(th)

# for th in threads:
#     th.start()
# for th in threads:
#     th.join()

end = time.time()
print(f'Time taken: {end-start} Seconds')