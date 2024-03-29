from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard',IndexView.as_view(), name='index'),
    path('add-company',AddCompanyView.as_view(), name='add_company'),
    path('adduser',AddUserView.as_view(),name='adduser'),
    path('',LoginView.as_view(), name='login'),
    path('logout', LogoutView, name="logout" ),
    path('user-details',UserDetailsView.as_view(),name='user_details'),
    path('add-zone',AddZoneView.as_view(),name='add_zone'),
    path('update-user/<str:user_name>',UpdateUserView.as_view(),name='update_user'),
    path('update-company/<int:company_id>',UpdateCompanyView.as_view(),name='update_company'),
    path('delete-company',DeleteCompany.as_view(),name='delete_company'),
    path('delete-user',DeleteUser.as_view(),name='delete_user'),
    path('user-zone',ZoneDetailsView.as_view(),name='user_zone'),
    path('delete-zone',DeleteZone.as_view(),name='delete_zone'),
    path('update-zone/<str:zone_id>',UpdateZoneView.as_view(),name='update_zone'),
    path('add-sensor-type',AddSensorTypeView.as_view(),name='add_sensor_type'),
    path('sensor-type',SensorTypeView.as_view(),name='sensor_type'),
    path('delete-sensor-type',DeleteSensorType.as_view(),name='delete_sensor_type'),
    path('update-sensor-type/<int:sensor_type_id>',UpdateSensorType.as_view(),name='update_sensor_type'),
    path('sensors',SensorView.as_view(),name='sensors'),
    path('add-sensor',AddSensorView.as_view(),name='add_sensor'),
    path('workflow',WorkFlowView.as_view(),name='workflow'),
    path('update-sensor/<str:sensor_id>',UpdateSensor.as_view(),name='update_sensor'),
    path('delete-sensor',DeleteSensor.as_view(),name='delete_sensor'),
    path('add-workflow',AddWorkflow.as_view(),name='add_workflow'),
    path('update-workflow/<int:workflow_id>',UpdateWorkflow.as_view(),name='update_workflow'),
    path('delete-workflow',DeleteWorkflow.as_view(),name='delete_workflow'),
    path('object-sensor-mapping',ObjectSensorMapping.as_view(),name='object_sensor_mapping'),
    path('add-object-sensor-mapping',AddObjectSensorMapping.as_view(),name='add_object_sensor_mapping'),
	path('update-object-sensor-mapping<int:object_id>',UpdateObjectSensorMapping.as_view(),name='update_object_sensor_mapping'), 
	path('delete-object-sensor-mapping',DeleteObjectsensormap.as_view(),name='delete_object_sensor_mapping'), 
	path('object-transaction',Transaction.as_view(),name='object_transaction') ,
    path('object-detail',Detail.as_view(),name='object_detail'),
    path('filters',Filters.as_view(),name='filters')
]