import os

v2ray_path = "./v2ray/v2ray"

if os.path.isfile(v2ray_path):
    try:
        os.system(f"{v2ray_path} run")
    except OSError as e:
        print(f"Error running v2ray: {e}")
else:
    print(f"{v2ray_path} does not exist")
