# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Companymaster(models.Model):
    companyid = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    phonenumber = models.CharField(max_length=25, blank=True, null=True)
    mobilenumber = models.CharField(max_length=25, blank=True, null=True)
    emailid = models.CharField(max_length=50, blank=True, null=True)
    contactperson = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    permittedobjects = models.IntegerField(blank=True, null=True)
    permittedzones = models.IntegerField(blank=True, null=True)
    subscriptionstartdate = models.DateField(blank=True, null=True)
    subscriptionenddate = models.DateField(blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)
    activecompany = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companymaster'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Objectsensormapping(models.Model):
    objectid = models.AutoField(primary_key=True)
    objectname = models.CharField(max_length=50, blank=True, null=True)
    sensorid = models.ForeignKey('Sensormaster', models.DO_NOTHING, db_column='sensorid')
    workflowid = models.ForeignKey('Workflowmaster', models.DO_NOTHING, db_column='workflowid', blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    objectimagepath = models.CharField(max_length=100, blank=True, null=True)
    activerecord = models.CharField(max_length=1)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid')
    objecttypeid = models.ForeignKey('Objecttypemaster', models.DO_NOTHING, db_column='objecttypeid', blank=True, null=True)
    masterobject = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objectsensormapping'


class Objecttransaction(models.Model):
    transactionid = models.BigAutoField(primary_key=True)
    sensorname = models.CharField(max_length=50, blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    objectname = models.CharField(max_length=50, blank=True, null=True)
    zonename = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.IntegerField(blank=True, null=True)
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
    zoneid = models.CharField(max_length=50, blank=True, null=True)
    param6 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    entrydatetime = models.DateTimeField(blank=True, null=True)
    paramvalues = models.TextField(blank=True, null=True)  # This field type is a guess.
    objecttypeid = models.ForeignKey('Objecttypemaster', models.DO_NOTHING, db_column='objecttypeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objecttransaction'


class Objecttypemaster(models.Model):
    objecttypeid = models.AutoField(primary_key=True)
    objecttypename = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.IntegerField(blank=True, null=True)
    movingobject = models.CharField(max_length=1, blank=True, null=True)
    groupingrequired = models.CharField(max_length=1, blank=True, null=True)
    groupcount = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objecttypemaster'


class Objectzonedetails(models.Model):
    objectid = models.ForeignKey(Objectsensormapping, models.DO_NOTHING, db_column='objectid', primary_key=True)
    objectname = models.CharField(max_length=50, blank=True, null=True)
    zoneid = models.CharField(max_length=50, blank=True, null=True)
    zonename = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid', blank=True, null=True)
    updateddatetime = models.DateTimeField(blank=True, null=True)
    sensorid = models.CharField(max_length=20, blank=True, null=True)
    paramvalues = models.TextField(blank=True, null=True)  # This field type is a guess.
    zoneentrydatetime = models.DateTimeField(blank=True, null=True)
    objecttypeid = models.ForeignKey(Objecttypemaster, models.DO_NOTHING, db_column='objecttypeid', blank=True, null=True)
    dashboardlink = models.CharField(max_length=100, blank=True, null=True)
    activerecord = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objectzonedetails'


class Sensormaster(models.Model):
    sensorid = models.CharField(primary_key=True, max_length=20)
    sensorname = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid')
    sensortypeid = models.ForeignKey('Sensortypemaster', models.DO_NOTHING, db_column='sensortypeid', blank=True, null=True)
    paramtype1 = models.CharField(max_length=20, blank=True, null=True)
    paramtype2 = models.CharField(max_length=20, blank=True, null=True)
    paramtype3 = models.CharField(max_length=20, blank=True, null=True)
    paramtype4 = models.CharField(max_length=20, blank=True, null=True)
    paramtype5 = models.CharField(max_length=20, blank=True, null=True)
    activesensor = models.CharField(max_length=1)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)
    paramtype6 = models.CharField(max_length=20, blank=True, null=True)
    paramtypes = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sensormaster'


class Sensortypemaster(models.Model):
    sensortypeid = models.AutoField(primary_key=True)
    sensortypename = models.CharField(max_length=50, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid')

    class Meta:
        managed = False
        db_table = 'sensortypemaster'


class Usermaster(models.Model):
    username = models.CharField(primary_key=True, max_length=6)
    userfullname = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid')
    userpassword = models.CharField(max_length=100, blank=True, null=True)
    activeuser = models.CharField(max_length=1)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usermaster'


class Workflowmaster(models.Model):
    workflowid = models.AutoField(primary_key=True)
    workflowname = models.CharField(max_length=50, blank=True, null=True)
    zonedetails = models.TextField(blank=True, null=True)  # This field type is a guess.
    finalzoneid = models.CharField(max_length=20, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid')

    class Meta:
        managed = False
        db_table = 'workflowmaster'


class Zonemaster(models.Model):
    zoneid = models.CharField(primary_key=True, max_length=50)
    zonename = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.ForeignKey(Companymaster, models.DO_NOTHING, db_column='companyid')
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    zoneimagepath = models.CharField(max_length=100, blank=True, null=True)
    activezone = models.CharField(max_length=1)
    createddate = models.DateTimeField(blank=True, null=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zonemaster'
