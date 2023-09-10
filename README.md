# Introduction to v2rayLOVE

v2rayLOVE is a GUI (Graphical User Interface) tool for Linux that is used to configure v2ray. v2ray is a tool used to bypass network censorship and access blocked content, such as accessing foreign websites from within China.

The name "LOVE" stands for "Linux Open Visualization Extension," which reflects the tool's purpose of providing an open and visual interface for Linux users to configure v2ray more easily.

# Supported Platforms

v2rayLOVE currently supports the following Linux platforms:

- Ubuntu x86_64 Linux release 6.2.0.26 with Python 3.10.12
- Debian 12 x86_64 Linux release 6.1.0-10 with Python 3.11.2
- openSUSE x86_64 Linux release 5.14.21-150500.53 with Python 3.6.15
- CentOS 7 x86_64 Linux release 3.10.0-1160.71.1.el7 with Python 3.6.8
- CentOS Steam 9 x86_64 Linux release 5.14.0-361.el9 with Python 3.9.17

Other Linux versions have not been tested, but users can test and use v2rayLOVE if they have Python 3, tkinter, and requests installed.

# Screenshots

Below is v2rayLOVE running on various linux distributions:

- Ubuntu x86_64 Linux release 6.2.0.26 
<img width="640" alt="capture_004_02092023_160122" src="https://github.com/wapypoafiapro/v2rayLOVE/assets/143803363/080426a8-0f91-4523-9d84-e63e77f7c9bb">

- Debian 12 x86_64 Linux release 6.1.0-10 
<img width="640" alt="capture_002_02092023_160117" src="https://github.com/wapypoafiapro/v2rayLOVE/assets/143803363/54e07759-7988-4eea-a36d-9b8cdf33ab9a">

- openSUSE x86_64 Linux release 5.14.21-150500.53 
<img width="640" alt="capture_003_02092023_160120" src="https://github.com/wapypoafiapro/v2rayLOVE/assets/143803363/794cda93-a914-4672-8a2c-cdcf1ec177eb">

- CentOS 7 x86_64 Linux release 3.10.0-1160.71.1.el7 
<img width="640" alt="capture_005_02092023_160335" src="https://github.com/wapypoafiapro/v2rayLOVE/assets/143803363/ec7f2d69-71c3-4a9a-9e74-d382a97f850e">

# Installation and Usage

To install and use v2rayLOVE, follow these steps:

1. Open the terminal of your Linux distribution.

2. To download the v2rayLOVE package, go to the GitHub releases page and click on '`Source code(tar.gz)`' to download the tar.gz file.
- Please change `chas1kennyet` and `20230904` to your own repository instead, as the below link may be outdated:
  - `https://github.com/chas1kennyet/v2rayLOVE/releases/tag/20230904`
  - `https://github.com/chas1kennyet/v2rayLOVE/archive/refs/tags/20230904.tar.gz`
- For example, maybe your own repository is in the following format: `https://github.com/rywtutanota/v2rayLOVE/archive/refs/tags/20230910.tar.gz`

3. Open the terminal and enter the path of the `tar.gz` file, then extract the compressed package to `~/Desktop/v2rayLOVE/` using the following command:

   ```
   tar xvf *.tar.gz -C ~/Desktop/
   ```

   - If you select `.zip` file, then you should use the following command instead:
     ```
     unzip *.zip -d ~/Desktop/
     ```





4. Navigate to the v2rayLOVE directory using the following command:

   `cd ~/Desktop/v2rayLOVE-*/`

5. Check if your system has Python 3 installed and its version using the following command:

   `python3 --version`

   If Python 3 is not installed, use the following command to install it:

- Ubuntu: `sudo apt-get install python3 -y`
- CentOS: `sudo yum install python3 -y`
- openSUSE: `sudo zypper install python3 -y`
- Debian: `sudo apt-get install python3 -y`

6. Check if your system has tkinter and requests installed using the following command:

   `python3 get_os_and_modules.py`

   If they are not installed, use the following command to install them:

   `python3 install_tkinter.py`

7. Check again if tkinter and requests are installed using the following command:

   `python3 get_os_and_modules.py`

8. If everything is installed, run the following command to start v2rayLOVE:

   `python3 1.py`

9. In the pop-up window, enter the subscription address (e.g., `https://www.example.com/link/uvfjmmqzdw6qzffa?sub=3`) and click "`Update`".

10. If the subscription address is in the correct v2ray format, it will be decoded and displayed in the list.

11. Select the server you want to use from the list and click "`Set`".

12. v2ray will start running in the background when v2rayLOVE is launched and will stop when v2rayLOVE is closed.

13. When you use the '`proxy`' checkbox, v2rayLOVE remembers your choice.
Note that if you enable the proxy and find that Firefox cannot open Google.com, you may need to check your Firefox network settings. It should use the system proxy instead of None or Manual. If you use the system proxy, the GNOME settings for network will override Firefox, and Firefox may have bugs related to system proxy settings. To avoid this issue, you can follow the guide below to install the latest version of Firefox, especially if you are using an openSUSE-like distribution.

14. You can also choose to "`autostart`" v2rayLOVE by selecting the "`autostart`" checkbox, which will automatically launch v2rayLOVE when the system starts up.

## Change Proxy of Terminal

For Debian and openSUSE, changing the proxy only affects the new window of the terminal, not new tabs within one terminal window.

For CentOS 7 and Ubuntu, changing the proxy only affects the new terminal if you use right-click on the desktop.

You can use the following command to test terminal proxy settings:

`wget -O 1.html https://www.google.com`

## Installing Firefox from a `.tar.bz2` Archive on openSUSE

To install Firefox from a ``.tar.bz2`` archive on openSUSE, follow these steps:

1. Download the Firefox ``.tar.bz2`` archive from the official Mozilla website: https://www.mozilla.org/en-US/firefox/all/#product-desktop-release

2. Extract the archive to a directory of your choice using the following command:

```
tar xvf firefox-*.tar.bz2
```
This command will extract the contents of the archive to a new directory called `firefox`.

3. Move the `firefox` directory to a location of your choice, such as `/opt`:

```
sudo mv firefox /opt/
```
4. Delete a old symbolic link and create a new symbolic link to the `firefox` binary in the `/usr/bin` directory:

```
sudo rm /usr/bin/firefox
sudo ln -s /opt/firefox/firefox /usr/bin/firefox
```
This will allow you to run Firefox from the command line by simply typing `firefox`.

5. You should now be able to launch Firefox from the desktop launcher or by typing `firefox` in the terminal.

6. If you want to open Firefox from the application panel, you should first find the .desktop file. To do this, open a terminal and run the following command:

```
find /usr/share/applications/ -name 'firefox*.desktop' -type f -print
```

This command will list the full paths of all the Firefox desktop files in the `/usr/share/applications/` directory and its subdirectories.

Once you have found the .desktop file for the version of Firefox you want to use, open it in a text editor using the following command:

```
sudo vi /path/to/firefox.desktop
```

Replace `/path/to/firefox.desktop` with the full path to the .desktop file you found earlier.

In the text editor, find the `Exec` line and modify it to the following:

```
Exec=firefox --new-window %u
```

This will ensure that the new version of Firefox starts from the `/usr/bin/firefox` path instead of the old path.

Save the changes to the .desktop file and exit the text editor.

The next time you click the Firefox icon in the application panel, it should launch the new version of Firefox from the correct path.

   
