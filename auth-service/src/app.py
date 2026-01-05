import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

db_service_uri = os.getenv("DB_SERVICE_URI", "http://localhost:5000")

@app.route("/login", methods=["POST"])
def login():
    response = request.get_json()
    username = response["username"]
    password = response["password"]

    if not username or not password:
        return jsonify({'message': 'Please provide both username and password'}), 422

    json_request = {"username": username, "password": password}
    request_uri = f"{db_service_uri}db/check_credentials/"
    response = requests.post(request_uri, json=json_request)
    status_code = response.status_code
    print(status_code)
    if status_code == 200:
        return jsonify({'message': 'Logged in successfully'}), 200
    elif status_code >=500:
        return jsonify({'message': 'Server error'}), 500
    else:
        return jsonify({'message': "Login failed"}), 401

@app.route("/register", methods=["POST"])
def register():
    response = request.get_json()
    username = response["username"]
    password = response["password"]
    email = response["email"]

    if not username or not password or not email:
        return jsonify({'message': 'Please provide username, email and password'}), 422

    response = requests.post(f"{db_service_uri}db/register/", json=response)

    status = response.status_code
    if status == 201:
        return jsonify({'message': 'Registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), status
