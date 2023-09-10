import subprocess
import re
import sys

try:
    # Run get_os_and_modules.py and read the output
    output = subprocess.check_output(["python3", "get_os_and_modules.py"]).decode('utf-8')

    # Use regex to read os_v
    os_v = re.search(r"\nOperating System Dist: (\w+)\n", output)
    if os_v:
        os_v = os_v.group(1)
    else:
        raise AttributeError("Could not find Operating System in output")

    # Check the feedback to determine the current OS
    if "All required modules are installed" in output:
        print("All required modules are installed")
    else:
        if os_v == 'ubuntu':
            print("Ubuntu detected")
            subprocess.call(["sudo", "apt", "-y", "install", "python3-tk"])
        elif os_v == 'centos':
            print("CentOS detected")
            subprocess.call(["sudo", "yum", "-y", "install", "python3-tkinter"])
            subprocess.call(["sudo", "pip3", "install", "requests"])
        elif os_v == 'debian':
            print("Debian detected")
            subprocess.call(["sudo", "apt", "-y", "install", "python3-tk"])
        elif os_v == 'suse':
            print("SUSE detected")
            subprocess.call(["sudo", "zypper", "-n", "install", "python3-tk"])
        else:
            print("Unknown OS detected")
            print("\nPlease manually install python3 tkinter")
            sys.exit(1)

except subprocess.CalledProcessError as e:
    print("Error: Could not run get_os_and_modules.py")
    print("Details:", e)
    sys.exit(1)
except AttributeError as e:
    print("Error: Could not find Operating System in output")
    print("Details:", e)
    sys.exit(1)
except Exception as e:
    print("Error: An unexpected error occurred")
    print("Details:", e)
    sys.exit(1)

