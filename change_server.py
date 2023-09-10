#The code snippet below demonstrates how to call the current Python script from another Python script:
#---------------------------------------------------------------------------------------------------------------------
#import base64
#import subprocess

## Define the server information
#server_info = 'trojan://aaa-111-222-333-bbb@ccc.ccc.ccc:443?sni=ddd.ddd.ddd# A丨A丨A丨A'

## Encode the server information in Base64
#base64_server_info = base64.b64encode(server_info.encode('utf-8')).decode('utf-8')

## Call {current file name}.py with the encoded server information as a command-line argument
#subprocess.run(['python3', '{current file name}.py', f'serverinfo={base64_server_info}'])
#---------------------------------------------------------------------------------------------------------------------

# This is a script that modifies the 'config.json' file based on the provided server information.
# It reads the server information from the command-line argument, decodes it from Base64, and extracts the address,
# server name, and password using regular expressions. The extracted values are then used to update the 'config.json'
# file with the modified data.


import base64
import json
import re
import sys

# Read the config.json file
try:
    with open('./v2ray/config.json', 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    print('Error: config.json file not found')
    sys.exit(1)
except json.JSONDecodeError:
    print('Error: invalid JSON format in config.json')
    sys.exit(1)

# Get the server information from the command-line argument
try:
    if len(sys.argv) > 1:
        server_info = sys.argv[1].split('=')[1]
    else:
        raise IndexError
except IndexError:
    print('Error: serverinfo parameter not found')
    sys.exit(1)

# Add padding characters to the end of the string
while len(server_info) % 4 != 0:
    server_info += '='

# Decode the server information from Base64
try:
    decoded_server_info = base64.b64decode(server_info).decode('utf-8')
except base64.binascii.Error:
    print('Error: invalid Base64 encoding')
    sys.exit(1)

# Extract the address, server name, and password using regex
try:
    password = re.search(r'trojan://(.+?)@', decoded_server_info).group(1)
    server_name = re.search(r'sni=(.+?)#', decoded_server_info).group(1)
    address = re.search(r'@(.+?):', decoded_server_info).group(1)
    port = re.search(r':(\d+?)\?', decoded_server_info).group(1)
except AttributeError:
    print('Error: invalid server information')
    sys.exit(1)

print('Password:', password)
print('Server Name:', server_name)
print('Address:', address)
print('Port:', port)

# Make the desired changes to the config data
config_data['outbounds'][0]['settings']['servers'][0]['address'] = address
config_data['outbounds'][0]['settings']['servers'][0]['port'] = int(port)
config_data['outbounds'][0]['streamSettings']['tlsSettings']['serverName'] = server_name
config_data['outbounds'][0]['settings']['servers'][0]['password'] = password

# Write the modified data back to the file
try:
    with open('./v2ray/config.json', 'w') as file:
        json.dump(config_data, file, indent=4)
        print('Config data written to config.json with indentation')        
except FileNotFoundError:
    print('Error: config.json file not found')
    sys.exit(1)
except PermissionError:
    print('Error: permission denied to write config.json')
    sys.exit(1)
