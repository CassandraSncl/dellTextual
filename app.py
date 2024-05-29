from flask import Flask, request, render_template, jsonify
import subprocess
import json, os

app = Flask(__name__)

def execute_script(script_name, input_data):
    result = subprocess.run(['python', f'scripts/mode_{script_name}.py', input_data], capture_output=True, text=True)
    print(result)
    print(os.getenv("ai"))
    print(result.stdout)
    output = json.loads(result.stdout)  # Charger la sortie JSON
    return output['result']

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_data = request.json.get('input')
    mode = request.json.get('mode')
    
    if mode == 'Movie':
        output = execute_script('movie', input_data)
    elif mode == 'People':
        output = execute_script('person', input_data)
    elif mode == 'Series':
        output = execute_script('series', input_data)
    else:
        output = 'Invalid mode'
    
    return jsonify({'output': output})


@app.route('/load_json', methods=['GET'])
def load_json():
    json_file_path = os.path.join('data', 'actuel.json')
    
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
