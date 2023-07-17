import json
from flask import Flask, request
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
        
        try:
            # Parse 'user' and 'poll' from the JSON payload
            data = request.json
            user = data.get('user')
            poll = data.get('poll')
            print(f'user: {user}')
            print(f'poll: {poll}')
            
            # Save user data to a JSON file
            with open('user_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f'Error parsing JSON: {e}')
            import traceback
            traceback.print_exc()
            return 'Error parsing JSON', 400
            
        # Execute the Python script as a subprocess
        result = subprocess.run(['python', 'apiDev.py'], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            return f'Script executed successfully.\nOutput:\n{output}'
        else:
            error = result.stderr
            return f'Script execution failed.\nError:\n{error}'

    def run(self, host='0.0.0.0', port=1213):
        app.run(host=host, port=port)

if __name__ == '__main__':
    listener = ApiListener()
    listener.run()
