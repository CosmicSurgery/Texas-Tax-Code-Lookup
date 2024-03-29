import requests
import numpy as np

parameters = {
"street":"706 CIMARRON HILLS TRL W",
"city":"GEORGETOWN",
"state":"TX",
"postalcode":"78628",
"api_key":"65cf629eae4e0275450588arde0e50b"
}

# response = requests.get("https://gis.cpa.texas.gov/search", params=parameters)
response = requests.get("https://geocode.maps.co/search", params=parameters)

print(response.status_code)

# print(response.json()[0])

num_response = len(response.json())
coords = []
for k in response.json():
    coords.append((k['lat'], k['lon']))
    coords.append((np.round(float(k['lat']),6), np.round(float(k['lon']),6)))


print(coords)
# print(response.json())

