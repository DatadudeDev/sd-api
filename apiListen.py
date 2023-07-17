from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/execute_script', methods=['POST'])
def execute_script():
    script = request.files['script']
    script.save('script.py')

    # Execute the Python script as a subprocess
    result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
    
    if result.returncode == 0:
        output = result.stdout
        return f'Script executed successfully.\nOutput:\n{output}'
    else:
        error = result.stderr
        return f'Script execution failed.\nError:\n{error}'

if __name__ == '__main__':
    app.run()
