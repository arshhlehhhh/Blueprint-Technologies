import json
import sys
import os
import requests

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import StatementError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://blueprint:Super123@rds-blueprinttech.cgneknmmmjt1.us-east-1.rds.amazonaws.com:3306/Demo_Game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
CORS(app)


class DemoGame(db.Model):

    __tablename__ = 'Demo_Game'

    scenerio_id = db.Column(db.Integer(), primary_key = True)
    message = db.Column(db.String(4294000000), nullable = False)
    startDate = db.Column(db.String(255), nullable = False)
    endDate = db.Column(db.String(255), nullable = False)

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

@app.route("/DemoGame/GetScenerioWithPrice/<int:scenerio_id>")
def get_scenerio_w_price(scenerio_id):
    
    #Retrieve stock prices (call stocks api end point and provide start and end date of scenerio)
    #Obtain the JSON of stock prices
    #Sort JSON into categories and dates
    #Return sorted JSON to caller with historic data

    if (DemoGame.query.filter_by(scenerio_id=scenerio_id).first()):
        
        demoGame = [DemoGame.json() for DemoGame in DemoGame.query.filter_by(scenerio_id=scenerio_id)]

        startDate = demoGame[0]['startDate']
        endDate = demoGame[0]['endDate']
        message = demoGame[0]['message']

        
        serviceUrl = "http://0.0.0.0:5004/stocks/retrieveByDate/" +startDate

        response = requests.get(serviceUrl)
        output = jsonify( { "scenario_details": demoGame[0], "stocks": response.json()["Stocks"]} )
        return output

    return jsonify({"message": "Scenerio ID is invalid."}), 500

@app.route("/DemoGame/startDemo/<string:user_id>")
def start_demo(user_id):

    # Check user id if scenerio exists
    print("User ID = " + user_id)
    serviceURL = "http://0.0.0.0:5002/accountdemo/get_user_scenerio/" + user_id

    response = requests.get(serviceURL).json()
    currentScenerio = 1
    accountDemo = [{ "user_id": user_id, "scenerio_id": 1, "balance": 1000000.0, "holding": "" }]

    if (response['AccountDemo'] != []):
        accountDemo = response['AccountDemo']
        currentScenerio = accountDemo[0]['scenerio_id'] + 1
    
    output = (get_scenerio_w_price(currentScenerio)).json

    #process the stocks
    stocks = sort_stocks_to_categories(output["stocks"])

    #concate the output with accountDemo and send back

    return jsonify( { "demoUser": accountDemo[0], "demoDetails": output["scenario_details"], "stocks": stocks} ), 200

def sort_stocks_to_categories(response):

    categories = {}

    for i in response:
        if i["category"] in categories.keys():
            categories[i["category"]].append({"date": i["date"], "ticker": i["ticker"], "name": i["name"], "price": i["price"]})
        else:
            categories[i["category"]] = [{"date": i["date"], "ticker": i["ticker"], "name": i["name"], "price": i["price"]}]
    return categories
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)