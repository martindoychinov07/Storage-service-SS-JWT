import os
import json
from flask import Flask, render_template, request, jsonify, make_response
from flask_marshmallow import Marshmallow
from authentication import check_for_token
import jwt
import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
METADATA_FILE = 'metadata.json'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ma = Marshmallow(app)
app.config['SECRET_KEY'] = 'key'

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as file:
        json.dump(metadata, file, indent=4)

@app.route('/')
@check_for_token
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    description = request.form.get('description')
    file = request.files.get('inputFile')

    if not file:
        return jsonify({"error": "No file provided"}), 400

    if not description:
        return jsonify({"error": "Description is required"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    metadata = load_metadata()

    new_metadata = {
        'description': description,
        'file_name': file.filename,
        'file_path': file_path
    }
    metadata.append(new_metadata)

    save_metadata(metadata)

    return jsonify({"message": f"File '{file.filename}' uploaded successfully"})

if __name__ == '__main__':
    app.run(debug=True)
