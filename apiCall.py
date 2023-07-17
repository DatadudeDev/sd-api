import requests

url = 'http://localhost:5000/execute_script'
files = {'script': open('loop.py', 'rb')}

response = requests.post(url, files=files)

print(response.text)
