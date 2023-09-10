# Use this command to call the Python script with the ADD and PATH
# parameters: `python3 {current python script}.py ADD=1 PATH=$(
# {target python script}.py)` As the target python script's path is not
# the same as the caller, we first need to use the 'cd' command to enter
# the target python script's path and then use python3 to call the target
# python script. As the target python script may have many calls to
# other files using relative paths, it is important to use 'cd' before
# calling the Python script to avoid errors.

# Note that the current Python script and target Python script must be
# in the same path. You can call the current Python script from its own
# path or from another path. The script will get the current Python
# script's path and change the directory to it before calling the target
# Python script. This action is written to a bash script and called from
# there.

import os
import sys
import re
import traceback

########################################
# Check the number of arguments passed to the script
########################################

PARAMETER_NUM = 2
PARA_REGEX = ['^ADD=(\d{1})$', '^PATH=([0-9a-zA-Z_-]{1,10}\.py)$']
PARA_EXPLAIN = '\nYou can use \n"python3 {current script name}.py ADD=1 PATH=12345.py"\nto run this script.'

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
        raise ValueError(f"Error 2: {e}")

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
    ADD = int(para_regex_[0])
    if ADD not in [0, 1]:
        raise ValueError("Error 3: ADD parameter must be 0 or 1")
except ValueError as e:
    print(f"Error 4: {e}")
    print(f"{PARA_EXPLAIN}")
    sys.exit(1)
    
########################################
# End of argument checking section
########################################

# Get the current directory and the path to the autostart_v2ray_love.sh script
current_dir = os.path.dirname(os.path.abspath(__file__))
autostart_v2ray_love_script_path = os.path.join(current_dir, "autostart_v2ray_love.sh")

# Initialize the ADD and E_PATH variables
ADD = para_regex_[0]
E_PATH = para_regex_[1]

# Construct the content of the autostart_v2ray_love.sh script
autostart_v2ray_love_script_content = f"""#!/bin/bash

cd "{os.path.dirname(os.path.realpath(__file__))}"
python3 {E_PATH}

"""

# Attempt to create the autostart_v2ray_love.sh script file and write the script content to it
try:
    with open(autostart_v2ray_love_script_path, "w") as f:
        f.write(autostart_v2ray_love_script_content)

    print(f"{autostart_v2ray_love_script_path} has been created")
except (FileNotFoundError, PermissionError) as e:
    print(f"Error: Could not create autostart_v2ray_love.sh: {e}")
    traceback.print_exc()
    sys.exit(1)

# Attempt to make the autostart_v2ray_love.sh script executable
try:
    os.chmod(autostart_v2ray_love_script_path, 0o755)
    print(f"{autostart_v2ray_love_script_path} has been made executable")
except (FileNotFoundError, PermissionError) as e:
    print(f"Error: Could not make autostart_v2ray_love.sh executable: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    # Create the .config/autostart directory if it doesn't exist
    autostart_dir = os.path.join(os.path.expanduser("~"), ".config", "autostart")
    if not os.path.exists(autostart_dir):
        os.makedirs(autostart_dir)
        print(f"Created: {autostart_dir}")
    else:
        print(f"Existed: {autostart_dir}")
except Exception as e:
    print(f"Error: Could not create {autostart_dir}: {e}")
    traceback.print_exc()
    sys.exit(1)

# Construct the path to the autostart_v2ray_love.desktop file
autostart_v2ray_love_desktop_path = os.path.join(autostart_dir, "autostart_v2ray_love.desktop")

# Construct the content of the autostart_v2ray_love.desktop file based on the value of the ADD variable
if ADD == '1':
    autostart_v2ray_love_desktop_content = f"""[Desktop Entry]
Type=Application
Name=autostart_v2ray_love
Exec=gnome-terminal -- /bin/bash -c '/bin/bash {autostart_v2ray_love_script_path}; exec bash'
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
elif ADD == '0':
    autostart_v2ray_love_desktop_content = f"""[Desktop Entry]
Type=Application
Name=autostart_v2ray_love
Exec=
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
else:
    print("Error: ADD parameter must be 0 or 1")
    sys.exit(1)

# Attempt to create the autostart_v2ray_love.desktop file and write the desktop file content to it
try:
    with open(autostart_v2ray_love_desktop_path, "w") as f:
        f.write(autostart_v2ray_love_desktop_content)
    if ADD == '1':
        print(f"Autostarted program added to .desktop file at: {autostart_v2ray_love_desktop_path}")
    else:
        print(f"Autostarted program removed from .desktop file at: {autostart_v2ray_love_desktop_path}")

except (FileNotFoundError, PermissionError) as e:
    print(f"Error: Could not create autostart_v2ray_love.desktop: {e}")
    traceback.print_exc()
    sys.exit(1)
