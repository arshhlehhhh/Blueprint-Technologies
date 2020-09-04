import json
import sys
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import StatementError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://blueprint:Super123@rds-blueprinttech.cgneknmmmjt1.us-east-1.rds.amazonaws.com:3306/Account_Demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)


class AccountDemo(db.Model):

    __tablename__ = 'Account_Demo'

    user_id = db.Column(db.String(45), primary_key = True)
    scenerio_id = db.Column(db.String(150), nullable = False)
    balance = db.Column(db.DECIMAL(10,0), nullable = False)
    holding = db.Column(db.String(45), nullable = False)

    def __init__(self, user_id, scenerio_id, balance, holding):
        self.user_id = user_id
        self.scenerio_id = scenerio_id
        self.balance = balance
        self.holding = holding

    def json(self):
        return {"user_id" : self.user_id, "scenerio_id" : self.scenerio_id, "balance" : self.balance, "holding": self.holding}

@app.route("/accountdemo/all")
def get_all():
    return jsonify({"AccountDemo": [AccountDemo.json() for AccountDemo in AccountDemo.query.all()]})

@app.route("/accountdemo/get_user_scenerio/<string:user_id>")
def get_user_scenerio(user_id):
    return jsonify( { "AccountDemo": [AccountDemo.json() for AccountDemo in AccountDemo.query.filter_by(user_id=user_id)] })

@app.route("/accountdemo/save_status/<string:user_id>", methods=['POST'])
def create_savepoint(user_id):
    data = request.get_json()
    
    if (AccountDemo.query.filter_by(user_id=user_id).first()):
        
        #Update entry with new scenerio_id/balance/holding
        accountdemo = AccountDemo.query.filter_by(user_id=user_id).first()
        accountdemo.scenerio_id = data['scenerio_id']
        accountdemo.balance = data['balance']
        accountdemo.holding = data['holding']

        try:
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred while updating the save point."}), 500

        return jsonify({"message": "Save point for {} has been updated.".format(user_id)}), 201

    else:

        #Create new entry with user_id/scenerio_id/balance/holding
        accountdemo = AccountDemo(user_id, **data)
    
        try:
            db.session.add(accountdemo)
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred while making a new save point."}), 500
        
        return jsonify({"message": "A new save point has been created for {}.".format(user_id)}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)