import requests
import tzlocal
from datetime import datetime
from requests.exceptions import RequestException
import pandas as pd
import numpy as np
from ftplib import FTP
import socket

df = pd.read_json('websites.json')

df.drop_duplicates(subset='URL', inplace=True)

# Get the local timezone dynamically
local_tz = tzlocal.get_localzone()

# Get current date and time in the local timezone
current_datetime = datetime.now(local_tz).strftime("%Y-%m-%dT%H:%M %Z")

def check_ftp_status(host):
    """
    Checks the status of an anonymous FTP site.

    Args:
        host (str): The hostname or IP address of the FTP server.

    Returns:
        bool: True if the FTP server is accessible, False otherwise.
    """
    try:
        ftp = FTP(host, timeout=5)  # Set a timeout to avoid indefinite waiting
        ftp.login() # Attempts anonymous login by default
        ftp.retrlines('LIST')  # Attempt a simple command to check connection
        ftp.quit()
        return True
    except (socket.timeout, OSError) as e:
        print(f"Error connecting to {host}: {e}")
        return f'{e}'#False
    except Exception as e:
         print(f"An unexpected error occurred: {e}")
         return f'{e}'#False

# Function to check URL availability
def check_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    if url.startswith("ftp"):
        return check_ftp_status(url)#np.nan
    try:
        response = requests.head(url, allow_redirects=True, timeout=20, headers=headers)
        return f'{response.status_code}'
    except RequestException as e:
        return f'{e}'

for url in df['URL']:
    status = check_url(url)
    print(f'{url}: {status}')
    column = f'status_{current_datetime}'
    df.loc[df['URL']==url,column] = [status]

df.to_csv('website_status.csv', columns=['URL', column], index=False)