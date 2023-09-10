# This script enables or disables GNOME and Terminal proxy settings
# based on the value of the 'GNOME_AND_TERMINAL_PROXY_ON'
# parameter. If the parameter is set to 1, the script enables the
# proxy settings using gsettings. If the parameter is set to 0, the
# script disables the proxy settings. Note that the 'http_proxy'
# environment variable is not set by this script, as it is controlled
# by the GNOME settings globally. To test the 'http_proxy' variable,
# use the command 'echo $http_proxy' in a new terminal window or
# after a reboot. Generally, the value of $http_proxy is set or not
# set in a new terminal window, and even after a reboot, it will
# impact new terminal windows too.

import os
import sys
import re

########################################
# Check the number of arguments passed to the script
########################################

PARAMETER_NUM = 1
PARA_REGEX = ['^PROXY=(\d{1})$']
PARA_EXPLAIN = '\nYou can use \n"python3 {current script name}.py PROXY=1 or 0"\nto run this script.'

def checkArg():
    try:
        # Get all the arguments passed to the script
        args = sys.argv

        # Get the number of arguments
        arg_num = len(args) - 1

        # Check if the number of arguments is equal to PARAMETER_NUM
        if arg_num != PARAMETER_NUM:
            raise ValueError(f"Error 1: Expected {PARAMETER_NUM} parameters, but got {arg_num}")

        # Extract the parameters from the arguments
        params = {}
        for i, arg in enumerate(args[1:]):
            params[i] = arg

        return params
    except Exception as e:
        raise ValueError(f"Error 2:{e}")

def checkArgRegex(param, regex):
    match = re.match(regex, param)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Error 0: Invalid parameter format: {param}")

try:
    params = checkArg()
    para_regex_ = [checkArgRegex(params[i], PARA_REGEX[i]) for i in range(PARAMETER_NUM)]

    # Print the parameter list
    for i, para in enumerate(para_regex_):
        print(f"para {i}: [{para}]")

    # Validate parameter values
    PROXY = int(para_regex_[0])
    if PROXY not in [0, 1]:
        raise ValueError("Error 3: PROXY parameter must be 0 or 1")
except ValueError as e:
    print(f"Error 4: {e}")
    print(f"{PARA_EXPLAIN}")
    exit(1)

########################################
# End of argument checking section
########################################

GNOME_AND_TERMINAL_PROXY_ON = PROXY

# Set or unset the proxy settings based on the parameter value
if GNOME_AND_TERMINAL_PROXY_ON == 1:
    # Set the proxy settings using gsettings
    os.system('gsettings set org.gnome.system.proxy mode "manual"')
    os.system('gsettings set org.gnome.system.proxy.http host "127.0.0.1"')
    os.system('gsettings set org.gnome.system.proxy.http port 10809')
    os.system('gsettings set org.gnome.system.proxy.https host "127.0.0.1"')
    os.system('gsettings set org.gnome.system.proxy.https port 10809')
    print('Added GNOME and Terminal proxy')
elif GNOME_AND_TERMINAL_PROXY_ON == 0:
    # Unset the proxy settings using gsettings
    os.system('gsettings set org.gnome.system.proxy mode "none"')
    print('Removed GNOME and Terminal proxy')
else:
    print('Error : The parameter must be 0 or 1')
    exit(1)
