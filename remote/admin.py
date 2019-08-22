from django.contrib import admin

# Register your models here.
from remote.models import *

admin.site.site_header = "My Factory Portal"
admin.site.site_title = "My Factory Portal"
admin.site.index_title = "Welcome to My Factory Portal"


class CompanymasterAdmin(admin.ModelAdmin):
    list_display = ('companyname', 'address1', 'address2', 'phonenumber', 'mobilenumber',
                    'emailid', 'contactperson', 'designation', 'permittedobjects', 'permittedzones',
                    'subscriptionstartdate', 'subscriptionenddate', 'createddate', 'updateddate',
                    'activecompany')
    search_fields = ('companyname', 'address1', 'address2', 'emailid', 'contactperson',
                     'designation', 'permittedzones')

    def get_readonly_fields(self, request, obj=None):
        return ['createddate', 'updateddate']


admin.site.register(Companymaster,CompanymasterAdmin)


class ObjectsensormappingAdmin(admin.ModelAdmin):
    # list_display = (
    #     'objectname', 'sensorid', 'zoneid', 'workflowid', 'startdate', 'enddate', 'objectimagepath', 'activerecord',
    #     'createddate', 'updateddate')

    # list_filter = (
    #     'sensorid', 'zoneid', 'workflowid', 'startdate', 'enddate')

    search_fields = (
        'objectname', 'objectimagepath', 'activerecord', 'startdate', 'enddate')

    def get_readonly_fields(self, request, obj=None):
        return ['updateddate', 'createddate']


admin.site.register(Objectsensormapping,ObjectsensormappingAdmin)


class ObjecttransactionAdmin(admin.ModelAdmin):
    list_display = ('sensorname', 'objectid', 'zonename', 'companyid',
                    'param1', 'param2', 'param3', 'param4', 'param5', 'batterylevel', 'latitude',
                    'longitude', 'rssi', 'sensorid', 'zoneid', 'param6', 'entrydatetime')
    search_fields = ('sensorname', 'sensorname', 'param1', 'param2', 'param3', 'param4')
    list_filter = ('objectid', 'zoneid', 'companyid',)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return ['entrydatetime']


admin.site.register(Objecttransaction,ObjecttransactionAdmin)


class SensormasterAdmin(admin.ModelAdmin):
    list_display = ('sensorname', 'companyid', 'sensortypeid', 'paramtype1', 'paramtype2',
                    'paramtype3', 'paramtype4', 'paramtype5', 'activesensor', 'createddate',
                    'updateddate', 'paramtype6')
    search_fields = ('sensorname', 'sensortypeid', 'paramtype1', 'paramtype2',
                     'paramtype3', 'paramtype4', 'paramtype5', 'activesensor', 'createddate',
                     'updateddate', 'paramtype6')

    def get_readonly_fields(self, request, obj=None):
        return ['updateddate', 'createddate']


admin.site.register(Sensormaster,SensormasterAdmin)
admin.site.register(Usermaster)

class SensortypemasterAdmin(admin.ModelAdmin):
    list_display = ('sensortypename', 'createddate', 'updateddate')
    search_fields = ('sensortypename', 'createddate', 'updateddate')

    def get_readonly_fields(self, request, obj=None):
        return ['updateddate', 'createddate']


admin.site.register(Sensortypemaster,SensortypemasterAdmin)


class ZonemasterAdmin(admin.ModelAdmin):
    list_display = ('zonename', 'companyid', 'latitude', 'longitude',
                    'zoneimagepath', 'activezone', 'createddate', 'updateddate')
    list_filter = ('zonename', 'companyid', 'latitude', 'longitude', 'activezone')

    search_fields = ('zonename', 'latitude', 'longitude', 'activezone')

    def get_readonly_fields(self, request, obj=None):
        return ['updateddate', 'createddate']


admin.site.register(Zonemaster,ZonemasterAdmin)


class ObjectzonedetailsAdmin(admin.ModelAdmin):
    list_display = ('objectname', 'zoneid', 'zonename', 'companyid', 'updateddatetime',)
    search_fields = ('objectname', 'zoneid', 'zonename',  'updateddatetime')
    list_filter = ('objectid', 'objectname', 'zoneid', 'zonename', 'companyid',)

    def get_readonly_fields(self, request, obj=None):
        return ['updateddatetime']


admin.site.register(Objectzonedetails,ObjectzonedetailsAdmin)
admin.site.register(Workflowmaster)
admin.site.register(Objecttypemaster)
