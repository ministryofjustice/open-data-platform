# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Courts(models.Model):
    name = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'courts'

class Crttype(models.Model):
    type = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'crttype'

class Ofgroup(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=1024, blank=True)
    class Meta:
        managed = False
        db_table = 'ofgroup'

class Sex(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=1024, blank=True)
    class Meta:
        managed = False
        db_table = 'sex'

class Ethcode(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=1024, blank=True)
    class Meta:
        managed = False
        db_table = 'ethcode'

class Offenses(models.Model):
    code = models.CharField(max_length=20, blank=True)
    act = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'offenses'

class PoliceForces(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'police_forces'

class Pleas(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'pleas'

class Outcomes(models.Model):
    multipers = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    amount1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    amount2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    amount3 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    amount4 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    crttype = models.CharField(max_length=2, blank=True)
    ofgroup = models.CharField(max_length=3, blank=True)
    force = models.CharField(max_length=2, blank=True)
    age = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    court = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    ethcode = models.IntegerField(blank=True, null=True)
    classctn = models.CharField(max_length=10, blank=True)
    plea = models.IntegerField(blank=True, null=True)
    proc = models.CharField(max_length=2, blank=True)
    disp1 = models.IntegerField(blank=True, null=True)
    disp2 = models.IntegerField(blank=True, null=True)
    disp3 = models.IntegerField(blank=True, null=True)
    disp4 = models.IntegerField(blank=True, null=True)
    clastype = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    guilty = models.IntegerField(blank=True, null=True)
    sent = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    offtyp = models.CharField(max_length=4, blank=True)
    ofclas = models.CharField(max_length=5, blank=True)
    notoff = models.IntegerField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'outcomes'
