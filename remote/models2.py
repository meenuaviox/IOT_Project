# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Companymaster(models.Model):
    companyid = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    phonenumber = models.CharField(max_length=25, blank=True, null=True)
    mobilenumber = models.CharField(max_length=25, blank=True, null=True)
    emailid = models.CharField(max_length=25, blank=True, null=True)
    contactperson = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    permittedobjects = models.IntegerField(blank=True, null=True)
    permittedzones = models.IntegerField(blank=True, null=True)
    subscriptionstartdate = models.DateField(blank=True, null=True)
    subscriptionenddate = models.DateField(blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)
    activecompany = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return self.companyname

    class Meta:
        managed = True
        db_table = 'companymaster'


class Zonemaster(models.Model):
    zoneid = models.CharField(primary_key=True, max_length=20)
    zonename = models.CharField(unique=True, max_length=50, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, on_delete=models.CASCADE,
                                  db_column='companyid', to_field='companyid')
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    zoneimagepath = models.CharField(max_length=100, blank=True, null=True)
    activezone = models.CharField(max_length=1, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.zonename

    class Meta:
        managed = False
        db_table = 'zonemaster'




class Sensormaster(models.Model):
    sensorid = models.CharField(primary_key=True, max_length=20, unique=True)
    sensorname = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, on_delete=models.CASCADE,
                                  db_column='companyid', to_field='companyid')
    sensortypeid = models.IntegerField(blank=True, null=True)
    paramtype1 = models.CharField(max_length=20, blank=True, null=True)
    paramtype2 = models.CharField(max_length=20, blank=True, null=True)
    paramtype3 = models.CharField(max_length=20, blank=True, null=True)
    paramtype4 = models.CharField(max_length=20, blank=True, null=True)
    paramtype5 = models.CharField(max_length=20, blank=True, null=True)
    activesensor = models.CharField(max_length=1, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)
    paramtype6 = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.sensorname

    class Meta:
        managed = False
        db_table = 'sensormaster'


class Objectsensormapping(models.Model):
    objectid = models.AutoField(primary_key=True)
    objectname = models.CharField(max_length=50, blank=True, null=True)
    sensorid = models.ForeignKey(Sensormaster, to_field='sensorid', db_column='sensorid', on_delete=models.CASCADE)
    zoneid = models.ForeignKey(Zonemaster, to_field='zoneid',
                               db_column='zoneid', on_delete=models.CASCADE)
    workflowid = models.IntegerField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    objectimagepath = models.CharField(max_length=100, blank=True, null=True)
    activerecord = models.CharField(max_length=1, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.objectname

    class Meta:
        managed = False
        db_table = 'objectsensormapping'


class Objecttransaction(models.Model):
    transactionid = models.BigAutoField(primary_key=True)
    sensorname = models.CharField(max_length=50, blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    objectname = models.CharField(max_length=50, blank=True, null=True)
    zonename = models.ForeignKey(Zonemaster, to_field='zonename',
                                 db_column='zonename', on_delete=models.CASCADE)
    companyid = models.ForeignKey(Companymaster, on_delete=models.CASCADE,
                                  db_column='companyid', to_field='companyid')
    param1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    param2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    param3 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    param4 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    param5 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    batterylevel = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    rssi = models.SmallIntegerField(blank=True, null=True)
    sensorid = models.CharField(max_length=20, blank=True, null=True)
    zoneid = models.CharField(max_length=20, blank=True, null=True)
    param6 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    entrydatetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.sensorname

    class Meta:
        managed = False
        db_table = 'objecttransaction'


class Sensortypemaster(models.Model):
    sensortypeid = models.AutoField(primary_key=True)
    sensortypename = models.CharField(max_length=50, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.sensortypename

    class Meta:
        managed = False
        db_table = 'sensortypemaster'
