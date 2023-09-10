import os
import subprocess
import time
import sys

# Kill Firefox if it is running
os.system("pkill firefox")

proxy_settings = {
    'network.proxy.backup.ssl': '""',
    'network.proxy.backup.ssl_port': '0',
    'network.proxy.http': '"127.0.0.1"',
    'network.proxy.http_port': '10809',
    'network.proxy.share_proxy_settings': 'true',
    'network.proxy.ssl': '"127.0.0.1"',
    'network.proxy.ssl_port': '10809',
    'network.proxy.type': '1',
    'network.trr.mode': '5'
}

#################################
# Parameters process
#################################

# Check the value of FIREFOX_PROXY_MANUAL_ON
try:
    parameter = sys.argv[1].split('=')[0]
    value = int(sys.argv[1].split('=')[1])
    
    if parameter != 'FIREFOX_PROXY_MANUAL_ON':
        raise ValueError("Invalid parameter name")
    
    if value not in [0, 1]:
        raise ValueError("Invalid parameter value")

except (IndexError, ValueError) as e:
    print(f"Error: {e}")
    sys.exit(1)

if value == 1:
    proxy_settings['network.proxy.type'] = '1'
    print('Proxy set to manual')
else:
    proxy_settings['network.proxy.type'] = '0'
    print('Proxy set to none')
    
    
#################################
# Parameters process
#################################

def changePref(prefs_path):
    try:
        # Open the prefs.js file and replace the specified preferences
        with open(prefs_path, 'r') as file:
            lines = file.readlines()

        with open(prefs_path, 'w') as file:
            for line in lines:
                f_d = 0
                for key, value in proxy_settings.items():
                    if key in line:
                        f_d = 1
                        break
                if not f_d:
                    file.write(line)  # no keys match, keep original keys

            for key, value in proxy_settings.items():  # add all the keys of 'network'
                file.write(f'user_pref("{key}", {value});\n')

        print(prefs_path + " Proxy settings updated.")
    except FileNotFoundError:
        print('Error: prefs.js file not found')
        sys.exit(1)
    except PermissionError:
        print('Error: permission denied to write prefs.js')
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def startFirefoxOneTimeAndShutdown():
    try:
        # Start Firefox in the background without any window appearing on the desktop
        subprocess.Popen(['firefox', '-headless'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for 3 seconds
        time.sleep(3)

        # Close Firefox without any error output
        subprocess.Popen(['pkill', 'firefox'])

        # Wait for 1 second
        time.sleep(1)
    except FileNotFoundError:
        print('Error: firefox command not found')
        sys.exit(1)
    except subprocess.SubprocessError:
        print('Error: failed to start or stop Firefox')
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

find_firefox_prefs = 0

# Find the prefs.js file from the root path
for root, dirs, files in os.walk('/home/', topdown=True):
    if 'prefs.js' in files:
        prefs_path = os.path.join(root, 'prefs.js')
        
        if 'firefox' in prefs_path:
            print("Code 1: There is a Firefox prefs.js file found at:", prefs_path)
            find_firefox_prefs = 1
            changePref(prefs_path)
        else:
            print("Code 2: There is a non-Firefox prefs.js found.")

if find_firefox_prefs == 0:
    print("There is no Firefox prefs.js file found.")
    startFirefoxOneTimeAndShutdown()
    print("Search prefs.js again...")    
    
    # Find the prefs.js file from the root path
    for root, dirs, files in os.walk('/home/', topdown=True):
        if 'prefs.js' in files:
            prefs_path = os.path.join(root, 'prefs.js')
            
            if 'firefox' in prefs_path:
                print("Code 1: There is a Firefox prefs.js file found at:", prefs_path)
                find_firefox_prefs = 1
                changePref(prefs_path)
                break
            else:
                print("Code 2: There is a non-Firefox prefs.js found.")

    if find_firefox_prefs == 0:
        print("Still unable to find Firefox prefs.js file.")
        sys.exit(1)
