import json
import sys
import os
import requests

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import StatementError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://blueprint:Super123@rds-blueprinttech.cgneknmmmjt1.us-east-1.rds.amazonaws.com:3306/Demo_Game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)


class DemoGame(db.Model):

    __tablename__ = 'Demo_Game'

    scenerio_id = db.Column(db.String(255), primary_key = True)
    message = db.Column(db.String(255), nullable = False)
    startDate = db.Column(db.DateTime(), nullable = False)
    endDate = db.Column(db.DateTime(), nullable = False)

    def __init__(self, scenerio_id, message, startDate, endDate):
        self.scenerio_id = scenerio_id
        self.message = message
        self.startDate = startDate
        self.endDate = endDate

    def json(self):
        return {"scenerio_id" : self.scenerio_id, "message" : self.message, "startDate" : self.startDate, "endDate": self.endDate}

@app.route("/DemoGame/all")
def get_all():
    return jsonify({"DemoGame": [DemoGame.json() for DemoGame in DemoGame.query.all()]})

@app.route("/DemoGame/GetScenerioWithPrice/<string:scenerio_id>")
def get_scenerio_w_price(scenerio_id):
    
    #Retrieve stock prices (call stocks api end point and provide start and end date of scenerio)
    #Obtain the JSON of stock prices
    #Sort JSON into categories and dates
    #Return sorted JSON to caller with historic data

    if (DemoGame.query.filter_by(scenerio_id=scenerio_id).first()):
        
        # demoGame = DemoGame.query.filter_by(scenerio_id=scenerio_id).first()
        # startDate = demoGame['startDate']
        # endDate = demoGame['endDate']
        # message = demoGame['message']

        startDate = "08-08-2020"
        endDate = "10-08-2020"
        message = "Tester"
        
        serviceUrl = "http://0.0.0.0:5004/stocks/retrieveByDate/"
        data = jsonify( { "startDate": startDate, "endDate": endDate } )

        response = requests.post(url=serviceUrl, json=data)

        #Sort JSON into categories and according to dates
        return response.json()

    return jsonify({"message": "Scenerio ID is invalid."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)