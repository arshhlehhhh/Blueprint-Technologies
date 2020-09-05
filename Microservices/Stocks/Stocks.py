import json
import sys
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import StatementError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://blueprint:Super123@rds-blueprinttech.cgneknmmmjt1.us-east-1.rds.amazonaws.com:3306/Stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)


class Stocks(db.Model):

    __tablename__ = 'Stocks'

    date = db.Column(db.DateTime(), primary_key = True)
    ticker = db.Column(db.String(255), primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float(), nullable = False)
    category = db.Column(db.String(255), nullable = False)

    def __init__(self, date, ticker, name, price, category):
        self.date = date
        self.ticker = ticker
        self.name = name
        self.price = price
        self.category = category

    def json(self):
        return {"date" : self.date, "ticker" : self.ticker, "name" : self.name, "price": self.price, "category": self.category}

@app.route("/stocks/all")
def get_all():
    return jsonify({"Stocks": [stocks.json() for stocks in Stocks.query.all()]})

@app.route("/stocks/retrieveByCategory/<string:category>")
def get_by_category(category):
    return jsonify( { "Stocks": [stocks.json() for stocks in Stocks.query.filter_by(category=category)] })

@app.route("/stocks/retrieveByDate/")
def get_by_date():
    data = request.get_json()
    return jsonify( { "Start Date": data['startDate'], "End Date": data['endDate'] } )
    
    # return jsonify( { "Stocks": [stocks.json() for stocks in Stocks.query.filter_by(date <= data['endDate'], date >= data['startDate'])] })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)