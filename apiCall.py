import requests

url = 'https://pc.datadude.dev/execute_script'
data = {'poll':'who should be president in 2024?','answer1': 'Donald Trump', 'answer2': 'Barack Obama','answer3':'Joe Biden','answer4':'Xi Xinping'}

response = requests.post(url, json=data)  # Use json parameter here

print(response.text)
