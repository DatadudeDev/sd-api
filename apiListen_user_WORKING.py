import json
from flask import Flask, request

app = Flask(__name__)

class ApiListener:
    def __init__(self):
        self.user = None

    @app.route('/execute_script', methods=['POST'])
    def execute_script():
        user = request.form.get('user')

        # Save user data to a JSON file
        data = {'user': user}
        with open('user_data.json', 'w') as f:
            json.dump(data, f)

        return user

    def run(self, host='localhost', port=5000):
        app.run(host=host, port=port)

if __name__ == '__main__':
    listener = ApiListener()
    listener.run()
