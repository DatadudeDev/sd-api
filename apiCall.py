import requests

url = 'http://localhost:1213/execute_script'
files = {'script': open('loop.py', 'rb')}
data = {'user':'Gabriel','poll':'Poll'}

response = requests.post(url, files=files, data=data)

print(response.text)
