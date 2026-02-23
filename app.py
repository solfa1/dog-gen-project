#!/usr/bin/python

import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from tasks import get_dog_pics

# --- Load environment variables ---
load_dotenv()

# --- Initialize Flask ---
flask_app = Flask(__name__, template_folder="templates")

# --- Configuration ---
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST', 'db')      # important for Docker
DB_PORT = os.environ.get('DB_PORT', '5432')

flask_app.config.update(
    SQLALCHEMY_DATABASE_URI=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# --- Initialize Database ---
db = SQLAlchemy(flask_app)

# --- Database Model ---
class DogTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(80))
    image_url = db.Column(db.String(255))

# --- Routes ---

@flask_app.route('/')
def home():
    return "Dog Generator API is running!"

@flask_app.route('/generate', methods=['POST'])
def generate_dogs():
    data = request.get_json()

    breed = data.get("breed")
    limit = data.get("limit", 1)

    if not breed:
        return jsonify({"error": "breed is required"}), 400

    task = get_dog_pics.delay(breed, limit)

    return jsonify({
        "task_id": task.id,
        "status": "processing"
    })

@flask_app.route('/dogs', methods=['GET'])
def list_dogs():
    dogs = DogTask.query.all()

    return jsonify([
        {"breed": d.breed, "image_url": d.image_url}
        for d in dogs
    ])

# --- Run Flask ---
if __name__ == "__main__":
    with flask_app.app_context():
        db.create_all()

    flask_app.run(host="0.0.0.0", port=5000)
