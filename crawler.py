import requests
from bs4 import BeautifulSoup

response = requests.get("https://gis.cpa.texas.gov/search")
print(response.status_code)

# print(response.json())