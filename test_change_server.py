import base64
import subprocess

# Define the server information
server_info = 'trojan://aaa-111-222-333-bbb@ccc.ccc.ccc:443?sni=ddd.ddd.ddd# A丨A丨A丨A'

# Encode the server information in Base64
base64_server_info = base64.b64encode(server_info.encode('utf-8')).decode('utf-8')

# Call .py with the encoded server information as a command-line argument
subprocess.run(['python3', 'change_server.py', f'serverinfo={base64_server_info}'])
