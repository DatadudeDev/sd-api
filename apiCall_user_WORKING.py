import requests

url = 'http://localhost:5000/execute_script'
files = {'script': open('apiDev.py', 'rb')}
data = {'user':'Gabriel'}

response = requests.post(url, files=files, data=data)

print(response.text)
