import requests

url = 'https://pc.datadude.dev/execute_script'
data = {'user':'Gabriel','poll':'Poll'}

response = requests.post(url, data=data)

print(response.text)
