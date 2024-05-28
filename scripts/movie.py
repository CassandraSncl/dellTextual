import sys
import json

def process_movie(input_data):
    # Traitement des données
    result = f"Movie script received: {input_data}"
    return result

if __name__ == "__main__":
    input_data = sys.argv[1]
    result = process_movie(input_data)
    print(json.dumps({"result": result}))  # Utilisez json.dumps pour formater la sortie
