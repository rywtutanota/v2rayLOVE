import subprocess

try:
    output = subprocess.check_output(["pgrep", "v2ray"])
    pids = [int(pid) for pid in output.decode("utf-8").strip().split('\n')]
    for pid in pids:
        subprocess.call(["kill", str(pid)])
    print(f"{len(pids)} instances of v2ray killed")
except subprocess.CalledProcessError as e:
    if e.returncode == 1:
        print("Error: v2ray is not running")
    else:
        print(f"Error killing v2ray: {e}")
except ValueError as e:
    print(f"Error parsing v2ray PID: {e}")
