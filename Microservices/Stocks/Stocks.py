import json
import sys
import os
import calendar
import requests

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import StatementError
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://blueprint:Super123@rds-blueprinttech.cgneknmmmjt1.us-east-1.rds.amazonaws.com:3306/Stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)
CORS(app)


class Stocks(db.Model):

    __tablename__ = 'Stocks'

    date = db.Column(db.String(255), primary_key = True)
    ticker = db.Column(db.String(255), primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Numeric(), nullable = False)
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
    try:
        jsonPayLoad = jsonify( { "Stocks": [stocks.json() for stocks in Stocks.query.filter_by(category=category)] })

        print(jsonPayLoad.json)
        finalDict = {}
        
        for element in jsonPayLoad.json["Stocks"]:
            #ticker, name
            if (element["ticker"] not in finalDict.keys()):
                finalDict[element["ticker"]] = {"name": element["name"]}

        return jsonify(finalDict)
    except:
        return jsonify( {"message": "Category does not exist"} )

@app.route("/stocks/retrieveByDate/<string:date>")
def get_by_date(date):
    try:
        return jsonify( { "Stocks": [stocks.json() for stocks in Stocks.query.filter_by(date = date)] } )
    except:
        return jsonify( {"message": "There are no sales on this day."} )
    
@app.route("/stocks/retrieveQuarter/<string:ticker>/<string:date>")
def get_quarter_result(ticker, date):

    key = "5bb3877196dfdde3adf163bd15ea59ee"

    datettime_obj = datetime.strptime(date, '%d-%b-%y')
    endDate = str(datettime_obj.date())
    
    days_in_month = calendar.monthrange(datettime_obj.year, datettime_obj.month)[1]
    newDate = datettime_obj - (timedelta(days=days_in_month) * 3)
    startDate = str(newDate.date())

    serviceURL = "https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?" + "apikey=" + key + "&from=" + startDate + "&" + "to=" + endDate
    print("API Call: " + serviceURL)
   
    try:
        response = requests.get(serviceURL)
        jsonPayLoad = response.json()
        histList = jsonPayLoad["historical"][::-1]
        histDict = {}
        for element in histList:
            histDict[element['date']] = element['close']
        return jsonify( histDict ), 200
    except:
        return jsonify( { "message": "unexpected error pulling historical data from API." } ),500

@app.route("/stocks/retrieveTickerStatistics/<string:ticker>")
def get_ticker_stats(ticker):
    key = "5bb3877196dfdde3adf163bd15ea59ee"
    finalJSON = {}
    
    try: 
        serviceURL = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?" + "apikey=" + key
        print("Calling: " + serviceURL)
        response = requests.get(serviceURL)
        
        jsonPayLoad = response.json()[0]
        print("Received")

        finalJSON["ebitda"] = jsonPayLoad["ebitda"]
        
        serviceURL = "https://financialmodelingprep.com/api/v3/key-metrics/" + ticker + "?" + "apikey=" + key
        print("Calling: " + serviceURL)
        response = requests.get(serviceURL)
        
        jsonPayLoad = response.json()[0]
        print("Received")

        finalJSON["peRatio"] = jsonPayLoad["peRatio"]
        finalJSON["priceToSalesRatio"] = jsonPayLoad["priceToSalesRatio"]
        finalJSON["enterpriseValueOverEBITDA"] = jsonPayLoad["enterpriseValueOverEBITDA"]
        finalJSON["interestCoverage"] = jsonPayLoad["interestCoverage"]

        serviceURL = "https://financialmodelingprep.com/api/v3/financial-growth/" + ticker + "?" + "apikey=" + key
        print("Calling: " + serviceURL)
        response = requests.get(serviceURL)
        
        jsonPayLoad = response.json()[0]
        print("Received")

        finalJSON["threeYRevenueGrowthPerShare"] = jsonPayLoad["threeYRevenueGrowthPerShare"]
        finalJSON["threeYOperatingCFGrowthPerShare"] = jsonPayLoad["threeYOperatingCFGrowthPerShare"]
        finalJSON["threeYNetIncomeGrowthPerShare"] = jsonPayLoad["threeYNetIncomeGrowthPerShare"]
        finalJSON["threeYShareholdersEquityGrowthPerShare"] = jsonPayLoad["threeYShareholdersEquityGrowthPerShare"]
        finalJSON["threeYDividendperShareGrowthPerShare"] = jsonPayLoad["threeYDividendperShareGrowthPerShare"]

        return jsonify(finalJSON)
    except:
        return jsonify( {"message": "There is an issue pulling {}'s information.".format(ticker)} )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)