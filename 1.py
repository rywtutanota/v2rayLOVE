import tkinter as tk
import base64
import requests
import os
import subprocess
import re
import sys

from requests.exceptions import Timeout, ProxyError
from tkinter import messagebox


true = 1
false = 0

global_listbox_slection_set = 0


def removeIllegalChars(line_text):
    # Generate a string of all Unicode characters within the BMP range
    bmp_chars = ''.join([chr(i) for i in range(0xFFFF + 1)])
    
    # Filter out illegal characters from line_text
    line_text = ''.join(char for char in line_text if char in bmp_chars)
    
    return line_text


def check_servers_txt(decoded_content):
    # Define the regular expressions to match
    ip_regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    domain_regex = r"[0-9a-zA-Z]{1,10}\.[0-9a-zA-Z]{1,10}"

    # Count the number of matches for each regular expression
    ip_count = len(re.findall(ip_regex, decoded_content))
    domain_count = len(re.findall(domain_regex, decoded_content))
    #print(ip_count)
    #print(domain_count)    
    # Return True if at least one match is found, False otherwise
    return ip_count > 1 or domain_count > 1


def proxy_switch():
    # Update the configuration dictionary with the new value
    config["proxy"] = proxy_var.get()
    set_proxy()
    # Write the updated configuration to the config.txt file
    with open("config.txt", "w") as f:
        f.write(f"subscribed_link={config['subscribed_link']}\n")
        f.write(f"proxy={str(config['proxy']).lower()}\n")
        f.write(f"autostart_v2ray={str(config['autostart_v2ray']).lower()}\n")


def autostart_v2ray_switch():
    # Update the configuration dictionary with the new value
    config["autostart_v2ray"] = autostart_v2ray_var.get()
    set_autostart()
    # Write the updated configuration to the config.txt file
    with open("config.txt", "w") as f:
        f.write(f"subscribed_link={config['subscribed_link']}\n")
        f.write(f"proxy={str(config['proxy']).lower()}\n")
        f.write(f"autostart_v2ray={str(config['autostart_v2ray']).lower()}\n")



def decode_utf8_string(url_encoded_str):
    decoded_str = ""
    decoded_str2 = ""
    i = 0
    j = 0
    while i < len(url_encoded_str):
        if url_encoded_str[i] == '%':
            hex_value = url_encoded_str[i+1:i+3]
            decoded_str += hex_value
            j += 1
            if j == 3:
                j = 0
                ch_char = bytes.fromhex(decoded_str).decode('utf-8')
                decoded_str2 += ch_char
                decoded_str = ""
            i += 3
        else:
            decoded_str += url_encoded_str[i]
            decoded_str2 += decoded_str
            decoded_str = ""
            i += 1
    return decoded_str2



def read_config():
    config = {
        "subscribed_link": "http://",
        "proxy": False,
        "autostart_v2ray": False,
    }
    
    try:
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                for line in f:
                    key, value = line.strip().split("=", 1)
                    if key == "subscribed_link":
                        config["subscribed_link"] = value
                    elif key == "proxy":
                        config["proxy"] = value.lower() == "true"
                    elif key == "autostart_v2ray":
                        config["autostart_v2ray"] = value.lower() == "true"
        else:
            with open("config.txt", "w") as f:
                f.write(f"subscribed_link={config['subscribed_link']}\n")
                f.write(f"proxy={str(config['proxy']).lower()}\n")
                f.write(f"autostart_v2ray={str(config['autostart_v2ray']).lower()}\n")
    
    except (IOError, ValueError) as e:
        print(f"Error 19: reading or writing config.txt: {e}")
    
    return config




def set_listbox():

    global global_listbox_slection_set
    
    # Read the subscribed link from the text box
    subscribed_link_text = subscribed_link.get()
    
    # Check if the subscribed link has only one line
    if '\n' not in subscribed_link_text:
        subscribed_link_text = subscribed_link_text.strip()
    else:
        # Get the first line of the subscribed link and strip it
        subscribed_link_text = subscribed_link_text.split('\n')[0].strip()
    
    # Delete the current text in the subscribed_link widget
    subscribed_link.delete(0, 'end')
    
    # Insert the processed subscribed link text into the subscribed_link widget
    subscribed_link.insert(0, subscribed_link_text)
    
    print(subscribed_link_text)
    
    try:

        # Set the proxies parameter to empty strings for both http and https protocols
        proxies = {
            "http": "",
            "https": "",
        }

        # Check if the http_proxy environment variable is set and update the proxies parameter
        if os.environ.get("http_proxy") is not None:
            proxies["http"] = os.environ.get("http_proxy")

        # Check if the https_proxy environment variable is set and update the proxies parameter
        if os.environ.get("https_proxy") is not None:
            proxies["https"] = os.environ.get("https_proxy")

        # Use requests to get the content of the subscribed link

        print("os.environ.get http_proxy:", os.environ.get("http_proxy"))
        print("os.environ.get https_proxy:", os.environ.get("https_proxy"))

        response = requests.get(subscribed_link_text, proxies=proxies, timeout=2)

        print(response)     

        content = response.content.decode('utf-8')

        # Use Base64 decoding to decode the content
        decoded_content = base64.b64decode(content).decode('utf-8')
        if(check_servers_txt(decoded_content)==false):
            print('Error : base64 decode error')
            return;
        # Write the decoded content into the servers.txt file
        with open("servers.txt", "w") as f:
            f.write(decoded_content)
            print('servers.txt written')

        # Update the configuration dictionary with the new values
        config["proxy"] = proxy_var.get()
        config["autostart_v2ray"] = autostart_v2ray_var.get()
        config['subscribed_link'] = subscribed_link_text

        # Write the updated configuration to the config.txt file
        with open("config.txt", "w") as f:
            f.write(f"subscribed_link={config['subscribed_link']}\n")            
            f.write(f"proxy={str(config['proxy']).lower()}\n")
            f.write(f"autostart_v2ray={str(config['autostart_v2ray']).lower()}\n")
            print('saved the subscribed_link to config.txt')

        # Clear the Listbox widget and insert the decoded content
        listbox.delete(0, tk.END)
        with open("servers.txt", "r") as f:
            for i, line in enumerate(f):
                line_text = line.strip().split("#")[1]
                line_text = decode_utf8_string(line_text)
                line_text=removeIllegalChars(line_text)
                listbox.insert(tk.END, f"{i+1}: {line_text}")
            print('updated listbox')
            
        focused = False

        with open("servers.txt", "r") as f:
            for i, line in enumerate(f):
                server_info_string = re.findall('(//.+?#)', line)
                if server_info_string:
                    server_info_string = server_info_string[0]
                    server_info_infile = subprocess.check_output(['python3', 'read_server.py']).decode().strip()
                    if server_info_string == server_info_infile:
                        listbox.see(i)  # focus the selected line
                        listbox.selection_set(i)  # select the highlighted line
                        global_listbox_slection_set = i
                        update_status_bar(line, status_bar)   
                        print('global_listbox_slection_set',global_listbox_slection_set)                                             
                        focused = True
                        print('Focused on current proxy server used')
            if not focused:
                print('Current proxy server used not found in the list box')                

    except Timeout:
        # Handle timeout error
        messagebox.showerror("Error", "Timeout: No response from the server")

    except ProxyError as e:
        # Handle proxy error
        
        messagebox.showerror("Error", "Proxy Error: Cannot connect to the proxy server"+ str(e))
        
    except Exception as e:
        # Handle all other types of errors
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def set_server():
    global global_listbox_slection_set
    try:
        print('global_listbox_slection_set',global_listbox_slection_set)
        # Get the highlighted line from the Listbox widget
        ii = listbox.curselection()
        if not ii:
            raise ValueError("No item selected")
        ii = ii[0]

        # Find the selected server information in the servers.txt file
        with open("servers.txt", "r") as f:
            for i, line in enumerate(f):
                if i == ii:
                    server_info = re.findall('(trojan://.+?#)', line)
                    
                    if not server_info:
                        raise ValueError("Invalid server information")
                    else:
                        update_status_bar(line, status_bar)
        
        # Check if server_info is valid before using it
        if not server_info:
            raise ValueError("Invalid server information")
        
        server_info=server_info[0]
        # Encode the server information in Base64
        base64_server_info = base64.b64encode(server_info.encode('utf-8')).decode('utf-8')

        # Call change_server.py with the encoded server information as a command-line argument
        subprocess.run(['python3', 'change_server.py', f'serverinfo={base64_server_info}'], check=True)

        global_listbox_slection_set = ii
        
                
        
    except ValueError as e:
        print(f"Error: {e}")
        listbox.selection_clear(0, tk.END)        
        listbox.selection_set(global_listbox_slection_set)  # select the highlighted line
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(global_listbox_slection_set)  # select the highlighted line

    except FileNotFoundError:
        print("Error: change_server.py not found")
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(global_listbox_slection_set)  # select the highlighted line
        
    except Exception as e:
        print(f"Error: {e}")
        listbox.selection_clear(0, tk.END)        
        listbox.selection_set(global_listbox_slection_set)  # select the highlighted line

    try:

        # Kill v2ray if it is running
        kill_process = subprocess.Popen(['python3', 'kill_v2ray.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kill_output, kill_error = kill_process.communicate()
        if kill_process.returncode != 0:
            print(f"Error killing v2ray: {kill_error.decode('utf-8').strip()}")

        # Start v2ray in the background
        run_process = subprocess.Popen(['python3', 'run_v2ray.py'], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

    pass

def set_autostart():
    try:
        if autostart_v2ray_var.get():
            # Call the add_autostart.py script with ADD=1 and PATH=__FILE__NAME__ arguments
            current_file_name = os.path.basename(__file__)
            subprocess.call(["python3", "add_autostart.py", "ADD=1", f"PATH={current_file_name}"])
        elif not autostart_v2ray_var.get():
            # Call the add_autostart.py script with ADD=0 and PATH=__FILE__NAME__ arguments
            current_file_name = os.path.basename(__file__)
            subprocess.call(["python3", "add_autostart.py", "ADD=0", f"PATH={current_file_name}"])
        else:
            raise ValueError('Error 15: Invalid value for autostart_v2ray_var')

    except subprocess.CalledProcessError as e:
        print(f'Error 16: executing add_autostart.py: {e}')
    except ValueError as e:
        print(f'Error 17: {e}')
    except Exception as e:
        print(f'Error 18: An unexpected error occurred: {e}')


def set_proxy():
    try:
        if proxy_var.get():

            # Using config_proxy.py alone is not sufficient to change the proxy settings of the current session.
             # Set the environment variables for HTTP and HTTPS proxies
            proxy_address = "http://127.0.0.1:10809"
            os.environ["http_proxy"] = proxy_address
            os.environ["https_proxy"] = proxy_address         


            # Call the config_proxy.py script with PROXY=1 argument to enable the proxy
            output = subprocess.check_output(["python3", "config_proxy.py", "PROXY=1"])
        elif not proxy_var.get():

            # Using config_proxy.py alone is not sufficient to change the proxy settings of the current session.            
            os.environ.pop("http_proxy", None)
            os.environ.pop("https_proxy", None)            

            # Call the config_proxy.py script with PROXY=0 argument to disable the proxy
            output = subprocess.check_output(["python3", "config_proxy.py", "PROXY=0"])
            
        else:
            raise ValueError('Error 14: Incorrect value for proxy_var')

        # Print the output of the config_proxy.py script
        print(output.decode())

    except subprocess.CalledProcessError as e:
        print(f'Error 13: executing config_proxy.py: {e}')
    except ValueError as e:
        print(f'Error 12: {e}')
    except Exception as e:
        print(f'Error 11: An unexpected error occurred: {e}')


#    try:
#        if proxy_var.get():            
#            subprocess.Popen(['python3', 'config_firefox.py', 'FIREFOX_PROXY_MANUAL_ON=1'])
#        else:                        
#            subprocess.Popen(['python3', 'config_firefox.py', 'FIREFOX_PROXY_MANUAL_ON=0'])
#    except subprocess.CalledProcessError as e:
#        print(f"Error 13.1: {e}")
#        
#    except FileNotFoundError:
#        print("Error 12.1: config_firefox.py not found")
#        
#    except Exception as e:
#        print(f"Error11.1: {e}")

#######################################
#######################################        

def on_closing():
    subprocess.run(['python3', 'kill_v2ray.py'])
    window.destroy()

# Create a GUI window
window = tk.Tk()
window.geometry("500x330")
window.title("V2rayLOVE")

# Bind the WM_DELETE_WINDOW event to on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)

# Run v2ray.py on startup
subprocess.Popen(['python3', 'run_v2ray.py'], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Read the configuration from the config file
config = read_config()

# Create a StatusBar widget to display the server info
class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def setText(self, text):
        self.label.config(text=text)

status_bar = StatusBar(window)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

def update_status_bar(line, status_bar):
    match = re.search(r'#(.+?)\n', line)
    if match:
        line_text=removeIllegalChars(match.group(1))
        status_bar.setText(line_text)

#######################################################

# Create a Listbox widget to display the list of items
listbox = tk.Listbox(window, selectmode=tk.SINGLE, height=10, width=50)
listbox.pack()

# Check if the servers.txt file exists, if not create an empty one
if not os.path.exists("servers.txt"):
    open("servers.txt", "w").close()

# Read the contents of the servers.txt file
try:
    with open("servers.txt", "r") as f:
        decoded_content = f.read()
except FileNotFoundError:
    print("Error: servers.txt file not found")
    decoded_content = ""

if(check_servers_txt(decoded_content)==true):
    # Fill the Listbox widget with the items from the servers.txt file
    try:
        with open("servers.txt", "r") as f:
            for i, line in enumerate(f):
                line_text = line.strip().split("#")[1]
                line_text = decode_utf8_string(line_text)
                line_text=removeIllegalChars(line_text)
                listbox.insert(tk.END, f"{i+1}: {line_text}")
        print('servers.txt readed.')
    except FileNotFoundError:
        print("Error: servers.txt file not found")

    try:
        with open("servers.txt", "r") as f:
            for i, line in enumerate(f):
                try:
                    server_info_string = re.findall('(//.+?#)', line)[0]
                except IndexError:
                    print("Error: regex pattern not found in line")
                    continue

                server_info_infile = subprocess.check_output(['python3', 'read_server.py']).decode().strip()

                if server_info_string == server_info_infile:
                    listbox.see(i)  # focus the selected line
                    listbox.selection_set(i)  # select the highlighted line
                    listbox.activate(i)

                    update_status_bar(line, status_bar)                           

                    global_listbox_slection_set = i
                    print('global_listbox_slection_set',global_listbox_slection_set)
        print('read_server.py to decide selected or not.')
    except FileNotFoundError:
        print("Error: servers.txt file not found")
else:
    listbox.insert(tk.END, f"{1}: {'no servers infomation'}")

# Change the selectmode option of the Listbox widget to "single"
listbox.config(selectmode=tk.SINGLE)



#######################################################

# Create a text box to input the subscribed link
subscribed_link = tk.Entry(window, width=50)

#######################################################
#######################################################

def paste_and_clear_selection(entry, n):
    # Check if there is a selection
    if entry.selection_present():
        # Delete the current selection
        entry.delete(tk.SEL_FIRST, tk.SEL_LAST)

        if not n:        
            entry.event_generate("<<Paste>>")
    else:
        if not n:
            entry.event_generate("<<Paste>>")

def select_all(event):
    # Select all the text in the Entry widget
    event.widget.select_range(0, tk.END)
    return "break"


# Create a context menu for the Entry widget
menu = tk.Menu(window, tearoff=0)
menu.add_command(label="Cut", command=lambda: subscribed_link.event_generate("<<Cut>>"))
menu.add_command(label="Copy", command=lambda: subscribed_link.event_generate("<<Copy>>"))
menu.add_command(label="Paste", command=lambda: paste_and_clear_selection(subscribed_link, 0))

# Attach the context menu to the Entry widget
subscribed_link.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))

# Bind the Ctrl+A event to select_all function
subscribed_link.bind("<Control-a>", select_all)

def paste(event):
    # Your custom paste functionality here
    paste_and_clear_selection(subscribed_link, 1)

# Bind the Ctrl+V event globally
window.bind_all("<Control-v>", paste)

#######################################################
#######################################################

subscribed_link.insert(0, config["subscribed_link"])
subscribed_link.pack()

# Create a button widget named 'update' to update the contents of the Listbox widget with the subscribed link
update_button = tk.Button(window, text="Update", command=set_listbox)
update_button.pack()

# Create a button named 'Set' to set the subscribed link
set_button = tk.Button(window, text="Set", command=set_server)
set_button.pack()

# Create a switch button to turn the proxy on or off
proxy_var = tk.BooleanVar(value=config["proxy"])
set_proxy()

    
proxy_switch = tk.Checkbutton(window, text="proxy", variable=proxy_var, command=proxy_switch)
proxy_switch.pack()

# Create an autostart checkbox for v2ray
autostart_v2ray_var = tk.BooleanVar(value=config["autostart_v2ray"])
set_autostart()


v2ray_autostart = tk.Checkbutton(window, text="Autostart v2ray", variable=autostart_v2ray_var, command=autostart_v2ray_switch)
v2ray_autostart.pack()

# Run the GUI window1
window.mainloop()
