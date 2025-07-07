from flask import Flask, request, render_template, jsonify
import requests
import csv
import os
from datetime import datetime

app = Flask(__name__)

HISTORY_FILE = "translation_history.csv"

# Ensure history file exists with headers
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'input_text_ja', 'output_text_zh'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'translated': ''})

    try:
        response = requests.post("https://libretranslate.com/translate", data={
            'q': text,
            'source': 'ja',
            'target': 'zh',
            'format': 'text'
        })
        translated = response.json().get('translatedText', '')

        # Save to history
        with open(HISTORY_FILE, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), text, translated])

        return jsonify({'translated': translated})
    except Exception as e:
        return jsonify({'translated': f'[Error] {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
