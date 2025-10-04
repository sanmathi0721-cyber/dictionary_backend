from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route('/define/<word>', methods=['GET'])
def define_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return jsonify({"definition": definition})
    else:
        return jsonify({"error": "Word not found"}), 404

if __name__ == '__main__':
    app.run()
