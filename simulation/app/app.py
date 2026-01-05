import re

from flask import Flask, request, make_response, jsonify
from datetime import date
import random, operator, time, hashlib

def create_header(X,response):
    value = random.randint(0,X)
    response.headers['exam'] = str(value)
    return value, response


def calc(X):
    return X

app = Flask(__name__, instance_relative_config=True)

def create_value(X, r):
    a = create_header(X,r)[1].headers
    b = calc(X)
    a.set('exam', str(b))
    return a

def create_app():
    return app

def create_secret(X,response):
    example = date.today()
    ran, _ = create_header(X,response)
    b = create_value(X,response)
    b['exam'] = "0"+(b['exam'][::-1])
    password = hashlib.md5(b['exam'].encode()).hexdigest()
    response.headers['exan'] = example.strftime("%Y")+example.strftime("%m")+example.strftime("%d")
    response.set_cookie('exam', str(4*(ran+6)/2-ran*2))
    response.set_cookie('exan', password)
    return response

def get_input_and_compute(op, name):
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    if name == "*":
        time.sleep(1)
    return op(a,b)

@app.route('/add')
def add():
    value = get_input_and_compute(operator.add, "+")
    return make_response(jsonify(s=value), 200)
    
@app.route('/sub')
def sub():
    value = get_input_and_compute(operator.sub, "-")
    return make_response(jsonify(s=value), 200)

@app.route('/mul')
def mul():
    value = get_input_and_compute(operator.mul, "*")
    return make_response(jsonify(s=value), 200)

@app.route('/div')
def div():
    value = get_input_and_compute(operator.truediv, "/")
    return make_response(jsonify(s=value), 200)

@app.route('/mod')
def mod():
    value = get_input_and_compute(operator.mod, "%")
    return make_response(jsonify(s=value), 200)

@app.route('/secret', methods=['GET'])
def get_secret():
    X = request.args.get('X', type = int)
    response = make_response(jsonify(exam=X), 200)
    return create_secret(X,response)

@app.route('/ex1', methods=["GET"])
def funcall():
    x: str = request.args.get('a', type = str)
    if x:
        # f(x) = d/c
        # d = digits in x, c = characters in x
        only_digits = re.sub(r'[^0-9]', '', x)
        only_alphabetic = re.sub(r'[^a-zA-Z]', '', x)

        n_of_digits = len(only_digits)
        n_of_alphabetic = len(only_alphabetic)

        if n_of_alphabetic >0 and n_of_digits >0:
            result = n_of_digits // n_of_alphabetic
            return jsonify({"s": result}), 200

    return jsonify({"s": "Invalid input"}), 400


#add your route here
