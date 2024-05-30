from flask import Flask, request, render_template, jsonify
import subprocess
import json, os
from langchain_openai.chat_models import ChatOpenAI
app = Flask(__name__)

def generate_summary_title(text):
    # Initialiser le modèle ChatOpenAI
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4-1106-preview",
        openai_api_base="http://localhost:8000/v1",
        openai_api_key="Not needed for local server"
    )
    
    # Créer le prompt pour générer un titre résumé
    prompt = f"Résumé le texte suivant en un titre concis : {text}"
    
    messages = [
        ("system", "You are a helpful assistant who creates a title of a few words based on the request. Without answering the question. Just the subject of the request"),
        ("human", text),
    ]
    response = llm.invoke(messages)
    
    # Retourner le titre résumé
    return response.content

def execute_script(script_name, input_data):
    result = subprocess.run(['python', f'scripts/mode_{script_name}.py', input_data], capture_output=True, text=True)
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

@app.route('/generate_title', methods=['POST'])
def get_title():
    question = request.json.get('question')
    title = generate_summary_title(question)
    return jsonify({'title': title})

@app.route('/load_json', methods=['GET'])
def load_json():
    json_file_path = os.path.join('data','actuel.json')
    
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/count_conversations', methods=['GET'])
def count_conversations():
    conversation_dir = os.path.join('data', 'conversation')
    try:
        files = os.listdir(conversation_dir)
        num_files = len(files)
        return jsonify({'num_files': num_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    content = request.json.get('content')
    numberchat = request.json.get('numberchat')
    file_path = os.path.join('data', 'conversation', f'conversation{numberchat}.txt')

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({'message': 'Conversation saved successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/load_conversation/<conversation_id>', methods=['GET'])
def load_conversation(conversation_id):
    file_path = os.path.join('data', 'conversation', f'{conversation_id}.txt')
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_conversation_titles', methods=['GET'])    
def get_conversation_titles():
    file_path = os.path.join('data', 'historique.txt')
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        conversations = []
        for line in lines:
            name, title = line.strip().split(', ')
            conversations.append({'name': name, 'title': title})
        return jsonify(conversations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

@app.route('/add_to_historique', methods=['POST'])
def add_to_historique():
    data = request.json
    name = data.get('name')
    title = data.get('title')
    historique_file_path = os.path.join('data','historique.txt')
    
    try:
        with open(historique_file_path, 'a') as file:
            file.write(f"{name}, {title}\n")
        return jsonify({'message': 'Added to historique successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
