from flask import Flask, request, render_template, jsonify
import subprocess
import json, os
from langchain_openai.chat_models import ChatOpenAI
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_conversation_history(input_data, conversation_id):

    file_path = os.path.join('data', 'conversation', f'conversation{conversation_id}.txt')
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()

            soup = BeautifulSoup(content, 'html.parser')

            conversation_history = []

            messages = soup.find_all('div', class_='message')

            for message in messages:
                if message.find('div', class_='human-message'):
                    human_text = message.find('p', class_='human-message-text').text
                    conversation_history.append(f'- Human: "{human_text}"\n')
                elif message.find('div', class_='bot-message'):
                    bot_text = message.find('p', class_='bot-message-text').text
                    conversation_history.append(f'- Bot: "{bot_text}"\n')

            historique_conversation = ' '.join(conversation_history)
            final_input = f"History : \n{historique_conversation}\n\nQuery: {input_data}\n\n"


            return final_input
    except Exception as e:
        return "Error: " + str(e)



@app.route('/generate_summary_title', methods=['POST'])
def generate_summary_title():
    text = request.json.get('text')
    try:
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
        return jsonify({'summary_title': response.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_conversation_title', methods=['POST'])
def update_conversation_title():
    data = request.json
    conversation_id = f"conversation{data.get('conversation_id')}"
    new_title = data.get('new_title')
    historique_file_path = os.path.join('data','historique.txt')

    try:
        with open(historique_file_path, 'r') as file:
            lines = file.readlines()

        with open(historique_file_path, 'w') as file:
            for line in lines:
                name, title = line.strip().split(', ')
                if name == conversation_id:
                    file.write(f"{name}, {new_title}\n")
                else:
                    file.write(line)

        return jsonify({'message': 'Title updated successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def execute_script(script_name, input_data, conversation_id):
    error_answer = "I'm sorry but I couldn't find the answer :("
    try:
        input_data = extract_conversation_history(input_data, conversation_id)
        result = subprocess.run(['python', f'scripts/mode_{script_name}.py', input_data], capture_output=True, text=True)
        
        # Check if the script execution failed
        if result.returncode != 0:
            print("Error during script execution:")
            print(result.stderr)
            return error_answer
        
        # Load the JSON output
        output = json.loads(result.stdout)
        
        # Check if 'result' key is present in the output
        if 'result' not in output:
            return error_answer
        
        return output['result']
    
    except json.JSONDecodeError:
        return error_answer
    except Exception:
        return error_answer

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_data = request.json.get('input')
    mode = request.json.get('mode')
    conversation_id = request.json.get('numberchat')
    
    if mode == 'Movie':
        output = execute_script('movie', input_data, conversation_id)
    elif mode == 'People':
        output = execute_script('person', input_data, conversation_id)
    elif mode == 'Series':
        output = execute_script('series', input_data, conversation_id)
    else:
        output = 'Select a mode please. Click on the buttons on the top right to switch'
    
    return jsonify({'output': output})

@app.route('/generate_title', methods=['POST'])
def get_title():
    question = request.json.get('question')
    title = generate_summary_title(question)
    return jsonify({'title': title})

@app.route('/load_json', methods=['GET'])
def load_json():
    json_file_path = os.path.join('data', 'actuel.json')
    
    if not os.path.exists(json_file_path):
        return jsonify("none")
    
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        os.remove(json_file_path)  # Supprime le fichier après l'avoir lu
        
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
        with open(file_path, 'w', encoding='utf-8', errors='replace') as file:
            file.write(content)
        return jsonify({'message': 'Conversation saved successfully.'})
    except Exception as e:
        print(str(e))
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
    



@app.route('/delete_conversation', methods=['POST'])
def delete_conversation():
    data = request.json
    conversation_id = data.get('conversation_id')
    conversation_file_path = os.path.join('data', 'conversation', f'{conversation_id}.txt')
    historique_file_path = os.path.join('data', 'historique.txt')

    try:
        # Supprimer le fichier de conversation
        if os.path.exists(conversation_file_path):
            os.remove(conversation_file_path)

        #Supprimer la ligne correspondante dans historique.txt
        with open(historique_file_path, 'r') as file:
            lines = file.readlines()

        with open(historique_file_path, 'w') as file:
            for line in lines:
                name, title = line.strip().split(', ')
                if name != conversation_id:
                    file.write(line)

        return jsonify({'message': 'Conversation deleted successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
if __name__ == '__main__':
    app.run(debug=True)

