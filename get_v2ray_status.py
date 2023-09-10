import subprocess
import sys

def check_process_running(process_name):
    try:
        output = subprocess.check_output(['ps', 'aux'], universal_newlines=True)
        for line in output.splitlines():
            if process_name in line:
                return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to check process status - {e}")
        sys.exit(1)

if check_process_running('v2ray'):
    print("v2ray is running")
else:
    print("v2ray is not running")
