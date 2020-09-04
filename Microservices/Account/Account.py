import json
import sys
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import StatementError
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://blueprint:Super123@rds-blueprinttech.cgneknmmmjt1.us-east-1.rds.amazonaws.com:3306/Account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)


class Account(db.Model):

    __tablename__ = 'Account'

    user_id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(45), nullable = False)
    name = db.Column(db.String(45), nullable = False)

    def __init__(self, user_id, password, name):
        self.user_id = user_id
        self.password = password
        self.name = name

    def json(self):
        return {"user_id" : self.user_id, "password" : self.password, "name" : self.name}

@app.route("/account/all")
def get_all():
    return jsonify({"Account": [Account.json() for Account in Account.query.all()]})

@app.route("/account/get_by_id/<string:user_id>")
def get_by_userid(user_id):
    return jsonify( { "Account": [account.json() for account in Account.query.filter_by(user_id=user_id)] })

@app.route("/account/<string:user_id>", methods=['POST'])
def create_user(user_id):
    if (Account.query.filter_by(user_id=user_id).first()):
        return jsonify({"message": "An account with User ID '{}' already exists.".format(user_id)}), 400

    data = request.get_json()
    password = sha256_crypt.encrypt(data["password"])
    print(password)
    account = Account(user_id, password, data["name"])
    
    try:
        db.session.add(account)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the account."}), 500
        
    return jsonify({"message": "An account with User ID '{}' has been created.".format(user_id)}), 201

@app.route("/account/authenticate/<string:user_id>", methods=['POST'])
def authenticate(user_id):
    if (Account.query.filter_by(user_id=user_id).first()):
        data = request.get_json()
        password = data['password']
        dbAccount = [account.json() for account in Account.query.filter_by(user_id=user_id)]
        print("Authenticate --", dbAccount)
        if (sha256_crypt.verify(password, dbAccount[0]['password'])):
            return jsonify({"message": "Successfully authenticated {}".format(user_id)}), 201
        return jsonify({"message": "Authenticated failed."}), 400
    return jsonify({"message": "An account with User ID '{}' already exists.".format(user_id)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)