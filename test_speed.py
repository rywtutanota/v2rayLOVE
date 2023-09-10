# This script measures the download speed of a file from a given URL.
# It uses the requests library to send HTTP requests and calculates the download speed and file size.

import requests
import time
import re
import os

def test_speed():
    if os.environ.get('http_proxy') and os.environ.get('https_proxy'):
        print('Proxy: enabled')
    else:
        print('Proxy: disabled')

    # Set the URL of the file to download
    url = 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/117.0/linux-x86_64/en-US/firefox-117.0.tar.bz2'

    # Define the regex pattern to match the server name
    pattern = r'https?://([\w.-]+)/'

    # Use the regex pattern to extract the server name from the URL
    match = re.search(pattern, url)

    if match:
        server_name = match.group(1)
        print(f"Server name: {server_name}")
    else:
        print('ERROR 1. Server name not found in URL')
        return

    try:
        # Send a HEAD request to get the file size
        response = requests.head(url, timeout=10)
        response.raise_for_status()  # Raise an exception if the response is not successful

        file_size = response.headers.get('Content-Length')
        if file_size is not None:
            file_size = int(file_size)  # in bytes
            print(f"File size: {file_size/1024/1024:.2f} MB")

        # Download the file for 10 seconds and measure the time it takes to download
        start_time = time.time()
        downloaded_bytes = 0

        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise an exception if the response is not successful
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    downloaded_bytes += len(chunk)
                    elapsed_time = time.time() - start_time 
                    if elapsed_time > 5:
                        break
                    if downloaded_bytes > 10 * 1024 * 1024:
                        break

        end_time = time.time()
        download_time = end_time - start_time
        download_speed_mbps = downloaded_bytes / (download_time * 1024 * 1024)

        # Print the download speed
        print(f"Download speed: {download_speed_mbps:.2f} MB/s")

        # Print the downloaded MB
        downloaded_mb = downloaded_bytes / 1024 / 1024
        print(f"Downloaded: {downloaded_mb:.2f} MB")

    except requests.exceptions.HTTPError as e:
        print(f"ERROR 2. HTTP error occurred: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR 3. Error connecting to the server: {e}")
    except requests.exceptions.Timeout as e:
        print(f"ERROR 4. Request timed out: {e}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR 5. An error occurred: {e}")

test_speed()
