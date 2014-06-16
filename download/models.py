from django.db import models

class Downloader(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)
    registration_date = models.DateTimeField('date registered')
