# This script reads the "config.json" file located in the "./v2ray/"
# directory, extracts the server address, port, server name, and
# password fields, and generates a feedback string using the following
# pattern:
#
#     //{password}@{address}:{port}?sni={server_name}#
#
# where:
# - {password} is the password used for authentication
# - {address} is the IP address or domain name of the server
# - {port} is the port number of the server
# - {server_name} is the SNI (Server Name Indication) value used for
#   TLS connections
#
# The feedback string is then printed to the console.

import json
import sys

def generate_feedback(address, port, server_name, password):
    feedback = f"//{password}@{address}:{port}?sni={server_name}#"
    return feedback

def read_config():
    try:
        with open("./v2ray/config.json", "r") as f:
            try:
                config_data = json.load(f)
                address = config_data["outbounds"][0]["settings"]["servers"][0]["address"]
                port = config_data["outbounds"][0]["settings"]["servers"][0]["port"]
                server_name = config_data["outbounds"][0]["streamSettings"]["tlsSettings"]["serverName"]
                password = config_data["outbounds"][0]["settings"]["servers"][0]["password"]
                feedback = generate_feedback(address, port, server_name, password)
                return feedback
            except KeyError:
                print("Error 0: Configuration file is missing required keys.")
                sys.exit(0)
            except json.JSONDecodeError:
                print("Error 1: Configuration file contains malformed JSON data.")
                sys.exit(0)
    except FileNotFoundError:
        print("Error 2: Configuration file not found.")
        sys.exit(0)

feedback = read_config()
print(feedback)
