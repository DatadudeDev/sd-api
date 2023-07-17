import json
from flask import Flask, request
import subprocess

app = Flask(__name__)

class ApiListener:
    def __init__(self):
        self.user = None

    @app.route('/execute_script', methods=['POST'])
    def execute_script():
        user = request.form.get('user')
        poll = request.form.get('poll')

        script = request.files['script']
        script.save('script.py')

        # Save user data to a JSON file
        data = {'user': user, 'poll': poll}
        with open('user_data.json', 'w') as f:
            json.dump(data, f)

        # Execute the Python script as a subprocess
        result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
        
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
