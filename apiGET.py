import requests

url = 'https://pc.datadude.dev/get_json_file'

response = requests.get(url)

if response.status_code == 200:
    url_json = response.json()
    print(url_json)
else:
    print(f"Failed to retrieve JSON file. Status code: {response.status_code}")
