from flask import Flask, request, render_template, jsonify
import subprocess
import json

app = Flask(__name__)

def execute_script(script_name, input_data):
    result = subprocess.run(['python', f'scripts/mode_{script_name}.py', input_data], capture_output=True, text=True)
    print(result.stdout)
    output = json.loads(result.stdout)  # Charger la sortie JSON
    return output['result']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_data = request.json.get('input')
    mode = request.json.get('mode')
    
    if mode == 'movie':
        output = execute_script('movie', input_data)
    elif mode == 'people':
        output = execute_script('person', input_data)
    elif mode == 'series':
        output = execute_script('series', input_data)
    else:
        output = 'Invalid mode'
    
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
