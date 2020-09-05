# from django.db import models
# from datetime import datetime 

# class Articles(models.Model):
#     timestamp = models.DateTimeField()
#     title = models.TextField()
#     temperatue = models.DecimalField(max_digits=12,decimal_places=2)
#     description = models.CharField(max_length=150)
#     city = models.CharField(max_length=150)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.timestamp = datetime.utcnow()
#         return super(Articles, self).save(*args, **kwargs)

# import boto3
# import json


# comprehend = boto3.client(service_name='comprehend', region_name='us-east-1', aws_access_key_id='AKIAJNVBM6Z7NHLR37VQ', aws_secret_access_key='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')
                
# text = "suicide is a great way to go"

# print('Calling DetectSentiment')
# print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
# print('End of DetectSentiment\n')