from flask import Flask, render_template, request, jsonify
import subprocess
import shlex
from flask_cors import CORS  # For Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    data = request.get_json()
    if 'code' in data:
        code = data['code']
        sanitized_code = sanitize_input(code)
        output = execute_command(sanitized_code)
        return jsonify({'output': output})
    return jsonify({'error': 'Invalid request'})

def sanitize_input(input_text):
    # Implement your input sanitization logic here
    # This is a simple example, you might need to do more depending on your use case
    return shlex.quote(input_text)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

if __name__ == '__main__':
    app.run(debug=True)
