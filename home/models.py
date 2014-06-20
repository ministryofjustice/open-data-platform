from django.db import models

class Feedback(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField('feedback date')

