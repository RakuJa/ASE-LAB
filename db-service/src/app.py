import os
import re
from typing import Mapping, Any

from cryptography.hazmat.primitives import hashes
from flask import Flask, request, jsonify
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from pymongo.synchronous.database import Database

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["mydatabase"]

app = Flask(__name__, instance_relative_config=True)

def ensure_user_indexes(db: Database):
    try:
        users = db["users"]

        users.create_index(
            [("username", ASCENDING)],
            unique=True,
            name="unique_username"
        )

        users.create_index(
            [("email", ASCENDING)],
            unique=True,
            name="unique_email"
        )
    except Exception:
        pass

ensure_user_indexes(db)

@app.route('/db/delete_database/', methods=['DELETE'])
def delete_database():
    db.drop_collection("users")
    ensure_user_indexes(db)
    return jsonify({'message': 'Database deleted'}), 200

@app.route('/db/register/', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 422

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 422

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return jsonify({'message': 'Invalid email address'}), 422

    insertion_result = create_new_user(db, username, email, password)
    if insertion_result == 201:
        json_message = {
            'message': 'User created successfully',
            'user': {
                'username': username,
                'email': email
            }
        }
    elif insertion_result == 409:
        json_message = {'message': 'User already exists'}
    else:
        json_message = {'message': 'Generic error creating user'}

    return jsonify(json_message), insertion_result


@app.route('/db/check_credentials/', methods=['POST'])
def check_credentials():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 422

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing required fields'}), 422

    if check_user_credentials(db, username, password):
        return jsonify({'message': 'Access granted'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


def create_new_user(db: Database[Mapping[str, Any] | Any], username: str, email: str, password: str) -> int:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(password.encode())
    hashed = digest.finalize()
    try:
        db["users"].insert_one({"username": username, "email": email, "password": hashed})
        return 201
    except DuplicateKeyError:
        return 409

def check_user_credentials(db: Database[Mapping[str, Any] | Any], username: str, password: str) -> bool:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(password.encode())
    hashed = digest.finalize()
    try:
        return db["users"].find_one({"username": username, "password": hashed}) is not None
    except Exception:
        return False