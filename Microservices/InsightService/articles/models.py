from django.db import models

# Create your models here.

class Articles(models.Model):
    articleFileName = models.TextField()
    datetime = models.DateField()

