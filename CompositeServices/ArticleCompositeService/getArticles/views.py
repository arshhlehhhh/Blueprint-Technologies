import decimal
from datetime import datetime 
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from botocore.config import Config
import boto3
# from getArticles.models import Forecast
    

class MainPage(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://192.168.1.226:8051/api/getarticles'
        latest = requests.request("GET", url)

        print(latest.text)
        try:
            timestamp = "{t.year}/{t.month:02d}/{t.day:02d}".format( t=latest.datetime)
        except:
            timestamp = "no latest"


        return render(
            request, 
            'index.html', 
            {'utc_update_time': timestamp})