import requests
import tzlocal
from datetime import datetime
from requests.exceptions import RequestException
import pandas as pd
import numpy as np

# List of NOAA URLs from the table above
urls = [
    "https://data.noaa.gov",
    "https://www.ncdc.noaa.gov/cdo-web/",
    "https://www.ncei.noaa.gov/",
    "https://www.weather.gov/",
    "https://www.fisheries.noaa.gov/resources/tech-and-tools",
    "https://tidesandcurrents.noaa.gov/",
    "https://coastwatch.noaa.gov/",
    "https://coris.noaa.gov/",
    "https://coast.noaa.gov/digitalcoast/",
    "https://registry.opendata.aws/noaa-swdi/",
    "https://www.nhc.noaa.gov/data/",
    "https://nomads.ncep.noaa.gov/",
    "https://ioos.noaa.gov/data/access-ioos-data/",
    "https://gml.noaa.gov/data/data.php",
    "https://nsidc.org/data/explore-data",
    "https://www.ncdc.noaa.gov/stormevents/",
    "https://www.class.noaa.gov/",
    "https://clearinghouse.marinedebris.noaa.gov/",
    "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/",
    "https://data.noaa.gov/datasetsearch/",
    "https://api.weather.gov/",
    "ftp://ftp.ncdc.noaa.gov/pub/data/",  # FTP URL (must be check manually)
    "https://www.nesdis.noaa.gov/data-research-services/data-collections"
]

df = pd.DataFrame({'url':urls})

# Get the local timezone dynamically
local_tz = tzlocal.get_localzone()

# Get current date and time in the local timezone
current_datetime = datetime.now(local_tz).strftime("%Y-%m-%dT%H:%M %Z")

# Function to check URL availability
def check_url(url):
    if url.startswith("ftp"):
        return np.nan
    try:
        response = requests.head(url, allow_redirects=True, timeout=20)
        return f'{response.status_code}'
    except RequestException as e:
        return f'{e}'

for url in df['url']:
    status = check_url(url)
    column = f'status_{current_datetime}'
    df.loc[df['url']==url,column] = [status]

df.to_csv('website_status.csv', index=False)