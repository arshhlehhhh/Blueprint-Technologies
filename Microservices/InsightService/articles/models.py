from django.db import models

# Create your models here.

class Articles(models.Model):
    distinctID = models.CharField(max_length=255)
    articleData = models.JSONField()
    timestamp = models.DateField()
    