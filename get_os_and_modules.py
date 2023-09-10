import platform
import importlib.util

def get_uninstalled_modules(os_name):
    modules = ['tkinter', 'base64', 'requests', 'os', 're', 'sys', 'subprocess', 'time', 'importlib', 'platform']
    uninstalled_modules = []

    for module in modules:
        try:
            importlib.import_module(module)
        except ImportError:
            uninstalled_modules.append(module)

    return uninstalled_modules

def echo_os_and_version():
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    os_machine = platform.machine()
    os_processor = platform.processor()
    os_python_version = platform.python_version()
    os_python_implementation = platform.python_implementation()
    os_more_version = platform.platform()

    print("System Information:")
    print("Operating System:", os_name)
    print("Release:", os_release)
    print("Version:", os_version)
    print("Machine:", os_machine)
    print("Processor:", os_processor)
    print("Python Version:", os_python_version)
    print("Python Implementation:", os_python_implementation)
    os = ""
    if "ubuntu" in os_version.lower() or "ubuntu" in os_more_version.lower():
        print("Current OS is Ubuntu")
        os = "ubuntu"
    elif "centos" in os_version.lower() or "centos" in os_more_version.lower():
        print("Current OS is CentOS")
        os = "centos"
    elif "debian" in os_version.lower() or "debian" in os_more_version.lower():
        print("Current OS is Debian")
        os = "debian"
    else:
        try:
            with open('/usr/lib/os-release') as file:
                for line in file:
                    if line.startswith('NAME'):
                        name_ = line.split('=')[1].strip().strip('"').lower()
                        if  "suse" in name_:
                            print("Current OS is SUSE")
                            os = "suse"
                            break
                        if "cent" in name_:
                            print("Current OS is CentOS")
                            os = "centos"
                            break;
                if os == "":
                    print("Unknown OS")
                    os = "unknown"                            
                            
                            
                            
                            
        except FileNotFoundError:
            pass


    uninstalled_modules = get_uninstalled_modules(os)

    return os, uninstalled_modules

# Example usage
os, uninstalled_modules = echo_os_and_version()
print(f"Operating System Dist: {os}")
if uninstalled_modules:
    print("The following modules are not installed:")
    for module in uninstalled_modules:
        print(module)
else:
    print("All required modules are installed")
