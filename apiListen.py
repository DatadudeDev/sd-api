import json
from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

class ApiListener:
    def __init__(self):
        self.user = None

    @app.route('/execute_script', methods=['POST'])
    def execute_script():
        # Log the raw request data
        raw_data = request.get_data()
        print(f'Raw request data: {raw_data.decode()}')
        
        poll = request.json.get('poll')
        answer1 = request.json.get('answer1')
        answer2 = request.json.get('answer2')
        answer3 = request.json.get('answer3')
        answer4 = request.json.get('answer4')       
        #print(f'user: {user}')
        #print(f'poll: {poll}')
        
        # Save user data to a JSON file
        data = {'prompt':poll,'answer1':answer1,'answer2':answer2,'answer3':answer3,'answer':answer4}
        with open('prompt.json', 'w') as f:
            json.dump(data, f)
            
        # Execute the Python script as a subprocess
        try:
            result = subprocess.run(['python', 'gen.py'], capture_output=True, text=True, check=True)
            
            # Read the content of image_url.json created by gen.py
            with open('image_url.json', 'r') as f:
                url_json = json.load(f)
            
            # Return the content of image_url.json as the API response
            return json.dumps(url_json)
            
        except subprocess.CalledProcessError as e:
            error = e.stderr.strip()
            return f'Script execution failed.\nError:\n{error}', 500

    @app.route('/get_json_file', methods=['GET'])
    def get_json_file():
        raw_data = request.get_data()
        print(f'Raw GET request data: {raw_data.decode()}')
        try:
            # Read the content of image_url.json
            with open('image_url.json', 'r') as f:
                url_json = json.load(f)

            # Return the JSON file as the response
            print(url_json)
            return url_json
        except FileNotFoundError:
            return 'JSON file not found.', 404

    def run(self, host='0.0.0.0', port=1213):
        app.run(host=host, port=port)

if __name__ == '__main__':
    listener = ApiListener()
    listener.run()
