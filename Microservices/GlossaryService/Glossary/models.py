from django.db import models

# Create your models here.

class Glossary(models.Model):
    term = models.TextField()
    description = models.TextField()
    actionable = models.TextField()