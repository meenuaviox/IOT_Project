from django.shortcuts import render
from django.views.generic import TemplateView, View,CreateView,ListView,DeleteView
from django.contrib.auth import authenticate
from django.shortcuts import redirect,HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
from .models import Companymaster, Usermaster, Zonemaster, Sensortypemaster,Sensormaster, Workflowmaster, Objectsensormapping, Objecttypemaster, Objecttransaction, Objectzonedetails
from django.contrib.auth import login, logout
import hashlib
import json
from remote.models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import uuid
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.utils import timezone
import operator
from django.db.models import Q
from django.template.loader import render_to_string
from functools import reduce

class IndexView(TemplateView):
	template_name='index.html'

	def get(self,request,*args, **kwargs):
		data=Companymaster.objects.all().order_by('-companyid')
		try:
			if request.user.is_staff and request.user.is_authenticated:
				return render(request,self.template_name,locals())
			else:
				return HttpResponseRedirect('/')
			
		except Exception as e:
			pass
		
class LoginView(TemplateView):
	template_name='login.html'
	def get(self,request,*args,**kwargs):
		if request.user.is_staff or request.user.is_authenticated:
			return HttpResponseRedirect('/dashboard')
		elif 'username' in request.session:
			return HttpResponseRedirect('/user-zone')
		else:
			return render(request,self.template_name,{})

	def post(self,request,*args,**kwargs):
		usern=request.POST.get('user')
		pas=request.POST.get('passwd')
		try:
			user_name=request.POST.get('user')
			password=request.POST.get('passwd')
			encrypted_password = encrypt_password(password)
			user = authenticate(username=usern, password=pas)
			if user:
				login(request,user)
				return HttpResponseRedirect('/dashboard')
			else:
				try:
					is_user=Usermaster.objects.get(username=user_name,userpassword=encrypted_password)
					if is_user:		
						request.session['username']=user_name
						return HttpResponseRedirect('/user-zone')
					else:
						messages.error(request,'Invaild details.')
						return HttpResponseRedirect('/')
				except Exception as e:
					print(str(e))
					messages.error(request,'Invaild Username or password.')
		except Exception as e:
				print(str(e))
		return render(request,self.template_name,{})

def LogoutView(request):
	logout(request)
	if 'username' in request.session:
		user= request.session['username']
		del request.session['username']
	return HttpResponseRedirect('/')

class AddCompanyView(TemplateView):
	template_name='add_company.html'
	def get(self,request,*args, **kwargs):
		if request.user.is_authenticated or 'username' in request.session:
			return render(request,self.template_name,locals())
		else:
			return HttpResponseRedirect('/')

	def post(self,request,*args,**kwargs):
		try:
			company=request.POST.get('cname')
			data=Companymaster(
			companyname=request.POST.get('cname'),
			address1=request.POST.get('address1'),
			address2=request.POST.get('address2'),
			phonenumber=request.POST.get('pnumber'),
			mobilenumber=request.POST.get('mnumber'),
			emailid=request.POST.get('email'),
			contactperson=request.POST.get('cperson'),
			designation=request.POST.get('desig'),
			permittedobjects=request.POST.get('pobjects'),
			permittedzones=request.POST.get('pzones'),
			subscriptionstartdate=request.POST.get('substart_date'),
			subscriptionenddate=request.POST.get('subend_date'),
			createddate=request.POST.get('company_createddate'),
			activecompany=request.POST.get('activec')
			)
			data.save()	
			messages.success(request,'Company added successfully.')	
			status='success'
		except Exception as e:
			print(str(e))
			messages.error(request,'Error!!! Please try again.')
			status='error'	
		return HttpResponseRedirect('dashboard')
		# return render(request,self.template_name,locals())


class UpdateCompanyView(TemplateView):
	template_name='update_company.html'
	def get(self,request,*args,**kwargs):
		try:
			company_id=kwargs.get('company_id')
			data=Companymaster.objects.get(companyid=company_id)
		except Exception as e:
			print(str(e))
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			companyid=request.POST.get('company_id')
			company_obj=Companymaster.objects.get(companyid=companyid)
			company_obj.companyname=request.POST.get('cname')		
			company_obj.address1=request.POST.get('address1')
			company_obj.address2=request.POST.get('address2')
			company_obj.phonenumber=request.POST.get('pnumber')
			company_obj.mobilenumber=request.POST.get('mnumber')
			company_obj.emailid=request.POST.get('email')
			company_obj.contactperson=request.POST.get('cperson')
			company_obj.designation=request.POST.get('desig')
			company_obj.permittedobjects=request.POST.get('pobjects')
			company_obj.permittedzones=request.POST.get('pzones')
			company_obj.subscriptionstartdate=request.POST.get('substart_date')
			company_obj.subscriptionenddate=request.POST.get('subend_date')
			company_obj.createddate=request.POST.get('cr_date')
			company_obj.activecompany=request.POST.get('activec')
			company_obj.save()	
		except Exception as e:
			print(str(e))
		return HttpResponseRedirect('/dashboard')

class DeleteCompany(View):
	def post(self, request, *args, **kwargs):
		response = {}
		company_id = request.POST.get("id")
		try:
			Companymaster.objects.get(companyid=int(company_id)).delete()
			response["status"]=True
		except Exception as e:
			print(str(e))
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")


class AddUserView(TemplateView):
	template_name='adduser.html'
	def get(self,request,*args,**kwargs):
		try:
			data=Companymaster.objects.filter(activecompany='Y').order_by('-companyid')
		except Exception as e:
			print(str(e))
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			username=request.POST.get('user')
			password = request.POST.get('pas')
			encrypted_password = encrypt_password(password)
			userfullname=request.POST.get('ufname')
			company=request.POST.get('selectedcompany')
			try:
				check=Usermaster.objects.get(username=username)
				messages.error(request,'Username already exists.')
				status='error'
				return render(request,self.template_name,locals())
			except Usermaster.DoesNotExist:
				usermaster=Usermaster(
					username=username,
					userfullname=userfullname,
					companyid_id=company,
					userpassword=encrypted_password

					)
				usermaster.save()
		except Exception as e:
			print(str(e))
		return HttpResponseRedirect('/user-details')

def encrypt_password(password):
		sha_signature=hashlib.sha256(password.encode()).hexdigest()
		return sha_signature

class UserDetailsView(TemplateView):
	template_name='user_details.html'
	def get(self,request,*args,**kwargs):
		user_details=Usermaster.objects.all().order_by('-username')
		return render(request,self.template_name,locals())

class UpdateUserView(TemplateView):
	template_name='update_user.html'
	def get(self,request,*args,**kwargs):
		try:
			data=Companymaster.objects.filter(activecompany='Y')
			username=kwargs.get('user_name')
			user_details=Usermaster.objects.get(username=username)
		except Exception as e:
			print(str(e)) 
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			username=kwargs.get('user_name')
			password=request.POST.get('pas')
			selectedcompany=request.POST.get("selectedcompany")
			user_obj=Usermaster.objects.get(username=username)
			user_obj.userfullname=request.POST.get('ufname')
			if password:		
				user_obj.userpassword=encrypt_password(password)
			user_obj.companyid_id=selectedcompany
			user_obj.save()	

		except Exception as e:
			print(str(e))
		return HttpResponseRedirect('/user-details')

class DeleteUser(View):
	def post(self, request, *args, **kwargs):
		response = {}
		user = request.POST.get("user")
		try:
			Usermaster.objects.get(username=user).delete()
			response["status"]=True
		except Exception as e:
			print(str(e))
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")


	
class AddZoneView(TemplateView):
	template_name='add_zone.html'
	def get(self,request,*args,**kwargs):
		try:
			comp=Companymaster.objects.filter(activecompany='Y').order_by('-companyid')	
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				comp=Companymaster.objects.get(companyid=companyid)						
		except Exception as e:
			print(str(e))
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):

		zoneid=request.POST.get('zoneid')
		latitude=request.POST.get('latitude')
		longitude=request.POST.get('longitude')
		zoneimagepath=request.POST.get('zoneimagepath')
		zonename=request.POST.get('zname')
		company=request.POST.get('selectedcompany')
		active=request.POST.get('active')

		try:
			zonemaster=Zonemaster(
				zoneid=zoneid,
				zonename=zonename,
				companyid_id=company,
				activezone=active,	
				latitude=latitude,
				longitude=longitude,
				zoneimagepath=zoneimagepath
			)
			zonemaster.save()			
		except Exception as e:
			print(str(e))
		return HttpResponseRedirect('/user-zone')


class ZoneDetailsView(TemplateView):
	template_name='user_zone.html'
	def get(self,request,*args,**kwargs):
		try:
			user_zone=Zonemaster.objects.filter(activezone='Y')

			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				user_zone=Zonemaster.objects.filter(companyid=companyid)
		except Exception as e:
			print(str(e))
		return render(request,self.template_name,locals())


class UpdateZoneView(TemplateView):
	template_name='update_zone.html'

	def get(self,request,*args,**kwargs):
		try:
			zone_id=kwargs.get('zone_id')
			data=Zonemaster.objects.get(zoneid=zone_id)
			company=Companymaster.objects.filter(activecompany='Y')
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				try:
					company=Companymaster.objects.get(activecompany='Y',companyid=companyid)
				except Exception as e:
					pass

		except Exception as e:
			pass
		return render(request,self.template_name,locals())
		
	def post(self,request,*args,**kwargs):
		try:
			zoneid=kwargs.get('zone_id')
			zone_obj=Zonemaster.objects.get(zoneid=zoneid)
			zone_obj.zonename=request.POST.get('zname')		
			zone_obj.companyid_id=request.POST.get('selectedcompany')
			zone_obj.activezone=request.POST.get('active')
			zone_obj.latitude=request.POST.get('update_latitude')
			zone_obj.longitude=request.POST.get('update_longitude')
			zone_obj.zoneimagepath=request.POST.get('update_zoneimagepath')
			zone_obj.save()	
		except Exception as e:
			pass
		return HttpResponseRedirect('/')


class DeleteZone(View):
	def post(self, request, *args, **kwargs):
		response = {}
		zone_id = request.POST.get("id")
		try:
			Zonemaster.objects.get(zoneid=zone_id).delete()
			response["status"]=True
		except Exception as e:
			pass
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")

class AddSensorTypeView(TemplateView):
	template_name='add_sensor_type.html'
	def get(self,request,*args,**kwargs):
		try:
			comp=Companymaster.objects.filter(activecompany='Y').order_by('-companyid')	
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				try:
					comp=Companymaster.objects.get(companyid=companyid)
				except Exception as e:
					pass
				
		except Exception as e:
			pass
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		sensortypename=request.POST.get('stname')
		company=request.POST.get('selectedcompany')
		try:
			sensortype=Sensortypemaster(
				sensortypename=sensortypename,
				companyid_id=company,
			)
			sensortype.save()		
		except Exception as e:
			pass
		return HttpResponseRedirect('/sensor-type')


class SensorTypeView(TemplateView):
	template_name='sensortypes.html'
	def get(self,request,*args,**kwargs):
		try:
			sensor_type=Sensortypemaster.objects.all()
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				sensor_type=Sensortypemaster.objects.filter(companyid=companyid)
		except Exception as e:
			print(str(e)) 
		return render(request,self.template_name,locals())

class UpdateSensorType(TemplateView):
	template_name='update_sensor_type.html'
	def get(self,request,*args,**kwargs):
		try:
			sensor_type_id=kwargs.get('sensor_type_id')

			data=Sensortypemaster.objects.get(sensortypeid=sensor_type_id)
			comp=Companymaster.objects.filter(activecompany='Y')
			if 'username' in request.session:
				user= request.session['username']
		except Exception as e:
			print(str(e)) 
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			sensortypeid=request.POST.get('sensor_type_id')
			sensor_type_obj=Sensortypemaster.objects.get(sensortypeid=sensortypeid)
			sensor_type_obj.sensortypename=request.POST.get('stname')	
			# sensor_type_obj.companyid_id=request.POST.get('selectedcompany')
			sensor_type_obj.save()	
		except Exception as e:
			print(str(e)) 
		return HttpResponseRedirect('/sensor-type')

class DeleteSensorType(View):
	def post(self, request, *args, **kwargs):
		response = {}
		sensor_type_id = request.POST.get("id")
		try:
			Sensortypemaster.objects.get(sensortypeid=sensor_type_id).delete()
			response["status"]=True
		except Exception as e:
			print(str(e)) 
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")

	
class SensorView(TemplateView):
	template_name='sensors.html'
	def get(self, request, *args, **kwargs):
		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				sensors=Sensormaster.objects.filter(companyid=companyid)
			elif request.user.is_staff:
				sensors=Sensormaster.objects.all()			
		except Exception as e:
			print(str(e))
		return render(request,self.template_name,locals())

class AddSensorView(TemplateView):
	template_name='add_sensor.html'

	def get(self, request, *args, **kwargs):
		
		try:
			sensortype=Sensortypemaster.objects.all().order_by('-sensortypeid')
			comp=Companymaster.objects.filter(activecompany='Y').order_by('-companyid')	
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				comp=Companymaster.objects.get(companyid=companyid)
				sensortype=Sensortypemaster.objects.filter(companyid=companyid)
		
		except Exception as e:
			pass
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			sensorid=request.POST.get('sensorid')
			sensorname=request.POST.get('sname')
			if request.user.is_staff:
				company=request.POST.get('selectedcompany')
			else:
				company=request.POST.get('compid')
			sensortype=request.POST.get('selectedsensortype')

			paramtypes=request.POST.get('paramtypes').split(',')
			paramtypes_list=[]
			for count,params in enumerate(paramtypes):
				param_dict={}
				param_dict['paramtype'+str(count+1)]=params
				paramtypes_list.append(param_dict)
			paramtypes=json.dumps(paramtypes_list)
			activesensor=request.POST.get('activesensor')
			sensor=Sensormaster(
				sensorid=sensorid,
				sensorname=sensorname,
				activesensor=activesensor,
				companyid_id=company,
				sensortypeid_id=sensortype,
				paramtypes=paramtypes,
				)
			sensor.save()			
		except Exception as e:
			pass
		return HttpResponseRedirect('/sensors')

class UpdateSensor(TemplateView):
	template_name='update_sensor.html'

	def get(self,request,*args,**kwargs):
		try:
			company=Companymaster.objects.filter(activecompany='Y')
			sensor_id=kwargs.get('sensor_id')
			data=Sensormaster.objects.get(sensorid=sensor_id)
			sensortype=Sensortypemaster.objects.all()
			if 'username' in request.session:
				user= request.session['username']
				user_obj=Usermaster.objects.get(username=user)
				companyid=user_obj.companyid.companyid
				try:
					company=Companymaster.objects.get(companyid=companyid)
				except Exception as e:
					print(e)
		except Exception as e:
			pass
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):

		try:
			sensorid=request.POST.get('sensorid')
			sensor_obj=Sensormaster.objects.get(sensorid=sensorid)
			sensor_obj.sensorname=request.POST.get('sname')	
			sensor_obj.companyid_id=request.POST.get('selectedcompany')
			sensor_obj.sensortypeid_id=request.POST.get('selectedsensortype')
			sensor_obj.activesensor=request.POST.get('activesensor')
			update_param_types=sensor_obj.paramtypes
			param_data=json.dumps(update_param_types)
			sensor_obj.paramtypes=param_data
			sensor_obj.save()	
		except Exception as e:
			pass
		return HttpResponseRedirect('/sensors')

class DeleteSensor(View):
	def post(self, request, *args, **kwargs):
		response = {}
		sensor_id = request.POST.get("id")
		try:
			Sensormaster.objects.get(sensorid=sensor_id).delete()
			response["status"]=True
		except Exception as e:
			print(str(e)) 
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")


class WorkFlowView(TemplateView):
	template_name='workflow.html'
	def get(self,request,*args,**kwargs):
		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				workflow=Workflowmaster.objects.filter(companyid=companyid)
			elif request.user.is_staff:
				workflow=Workflowmaster.objects.all()			
		except Exception as e:
			pass
		return render(request,self.template_name,locals())


class AddWorkflow(TemplateView):
	template_name='add_workflow.html'
	def get(self,request,*args,**kwargs):
		try:
			comp=Companymaster.objects.filter(activecompany='Y').order_by('-companyid')	
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				comp=Companymaster.objects.get(companyid=companyid)					
		except Exception as e:
			print(str(e))
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		workflowname=request.POST.get('workflowname')
		zonedetails=request.POST.get('zonedetails').split()
		finalzoneid=request.POST.get('finalzoneid')
		company=request.POST.get('selectedcompany')
		det={}
		
		for details in zonedetails:
			d={'key1':zonedetails}
			det.update(d)
		zonedetails = json.dumps(det)
		try:
			workflowmaster=Workflowmaster(
				workflowname=workflowname,
				zonedetails=zonedetails,
				finalzoneid=finalzoneid,
				companyid_id=company,
			)
			workflowmaster.save()

			messages.success(request,'workflow added successfully.')	
			status='success'		
		except Exception as e:
			messages.error(request,'Some error occur while adding workflow.')
			status='error'
			pass
		return render(request,self.template_name,locals())
		

class UpdateWorkflow(TemplateView):
	template_name='update_workflow.html'
	def get(self,request,*args,**kwargs):
		try:
			company=Companymaster.objects.filter(activecompany='Y')
			workflow_id=kwargs.get('workflow_id')
			data=Workflowmaster.objects.get(workflowid=workflow_id)

			if 'username' in request.session:
				user= request.session['username']
				try:
					user_obj=Usermaster.objects.get(username=user)
					companyid=user_obj.companyid.companyid
					company=Companymaster.objects.get(companyid=companyid)
				except Exception as e:
					pass
				
		except Exception as e:
			pass
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			workflowid=request.POST.get('workflowid')
			workflow_obj=Workflowmaster.objects.get(workflowid=workflowid)
			workflow_obj.workflowname=request.POST.get('workflowname')		
			workflow_obj.finalzoneid=request.POST.get('finalzoneid')
			workflow_obj.companyid_id=request.POST.get('selectedcompany')
			zone_details=request.POST.get('zonedetails')

			zonedetails=json.dumps(zone_details)
			workflow_obj.zonedetails=zonedetails
			workflow_obj.save()	
		except Exception as e:
			raise e
		return HttpResponseRedirect('/workflow')

class DeleteWorkflow(View):
	def post(self, request, *args, **kwargs):
		response = {}
		workflow_id = request.POST.get("id")
		try:
			Workflowmaster.objects.get(workflowid=workflow_id).delete()
			response["status"]=True
		except Exception as e:
			pass
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")

class ObjectSensorMapping(TemplateView):
	template_name='object_sensor_mapping.html'
	def get(self, request, *args, **kwargs):
		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				objectsensormapping=Objectsensormapping.objects.filter(companyid=companyid)
				sensors = Sensormaster.objects.filter(companyid=companyid).values("sensorid").distinct()
				workflows = Workflowmaster.objects.filter(companyid=companyid).values("workflowid","workflowname").distinct()
				objecttypes = Objecttypemaster.objects.filter(companyid=companyid).values("objecttypeid","objecttypename").distinct()	

			elif request.user.is_staff:

				objectsensormapping=Objectsensormapping.objects.all()
				sensors = Sensormaster.objects.values("sensorid").distinct()
				workflows = Workflowmaster.objects.values("workflowid","workflowname").distinct()
				objecttypes = Objecttypemaster.objects.values("objecttypeid","objecttypename").distinct()		
		except Exception as e:
			raise e
		return render(request,self.template_name,locals())

class filterSensorMappingData(View):

	def get(self,request,*args,**kwargs):

		response={}

		filter_workflow_name = request.GET.get("filter_workflow_name")
		filter_sensor_id = request.GET.get("filter_sensor_id")
		filter_object_type = request.GET.get("filter_object_type")
		radio_filter = request.GET.get("active")
		mapping_list=[]
		query_list = []

		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				objectsensormapping=Objectsensormapping.objects.filter(companyid=companyid)

				sensors = Sensormaster.objects.filter(companyid=companyid).values("sensorid").distinct()
				workflows = Workflowmaster.objects.filter(companyid=companyid).values("workflowid","workflowname").distinct()
				objecttypes = Objecttypemaster.objects.filter(companyid=companyid).values("objecttypeid","objecttypename").distinct()

				if filter_workflow_name:
					query_list.append(Q(workflowid_id=filter_workflow_name,companyid=companyid))
				if filter_sensor_id:
					query_list.append(Q(sensorid_id=filter_sensor_id,companyid=companyid))
				if filter_object_type:
					query_list.append(Q(objecttypeid_id=filter_object_type,companyid=companyid))
				if radio_filter and radio_filter == 'Y':
					query_list.append(Q(activerecord='Y',companyid=companyid))
				if radio_filter and radio_filter == 'N':
					query_list.append(Q(activerecord='N',companyid=companyid))

				if query_list:
					objectsensormapping = Objectsensormapping.objects.filter(reduce(operator.and_, query_list))
				else:
					objectsensormapping = Objectsensormapping.objects.filter(companyid=companyid)

			

			else:
				objectsensormapping=Objectsensormapping.objects.all()
				sensors = Sensormaster.objects.values("sensorid").distinct()
				workflows = Workflowmaster.objects.values("workflowid","workflowname").distinct()
				objecttypes = Objecttypemaster.objects.values("objecttypeid","objecttypename").distinct()

				if filter_workflow_name:
					query_list.append(Q(workflowid_id=filter_workflow_name))
				if filter_sensor_id:
					query_list.append(Q(sensorid_id=filter_sensor_id))
				if filter_object_type:
					query_list.append(Q(objecttypeid_id=filter_object_type))
				if radio_filter and radio_filter == 'Y':
					query_list.append(Q(activerecord='Y'))
				if radio_filter and radio_filter == 'N':
					query_list.append(Q(activerecord='N'))

				if query_list:
					objectsensormapping = Objectsensormapping.objects.filter(reduce(operator.and_, query_list))
				else:
					objectsensormapping = Objectsensormapping.objects.all()
					
			for data in objectsensormapping:
				mapping_dict={
				'objectname':data.objectname,
				'sensorname':data.sensorid.sensorname,
				'workflowname':data.workflowid.workflowname,
				'companyname':data.companyid.companyname,
				'status':data.activerecord,
				}
				mapping_list.append(mapping_dict) 
			if mapping_list:
				response['response_data']=mapping_list
				response['status']=True
			else:
				response['status']=False
		except Exception as e:
			response['status']=False
			raise e
		return HttpResponse(json.dumps(response),content_type="application/json")


	

class AddObjectSensorMapping(TemplateView):
	template_name='add_object_sensor_mapping.html'
	def get(self,request,*args,**kwargs):
		
		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				comp=Companymaster.objects.get(companyid=companyid)
				sensor=Sensormaster.objects.filter(companyid=companyid)
				workflow=Workflowmaster.objects.filter(companyid=companyid)
				objecttype=Objecttypemaster.objects.filter(companyid=companyid)
			else:
				sensor=Sensormaster.objects.all()
				workflow=Workflowmaster.objects.all()
				comp=Companymaster.objects.filter(activecompany='Y').order_by('-companyid')
				objecttype=Objecttypemaster.objects.all().order_by('-objecttypeid')
		except Exception as e:
			pass
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		objectname=request.POST.get('objectname')
		sensor=request.POST.get('selectedsensor')
		workflow=request.POST.get('selectedworkflow')
		objecttype=request.POST.get('selectedobjecttype')
		companyid=request.POST.get('selectedcompany')
		activerecord=request.POST.get('activerecord')	
		object_type = request.POST.get('object_type')
		if object_type:
			response = {}
			objecttypemaster = Objecttypemaster.objects.get(objecttypeid=object_type)
			
			unique_master = Objectsensormapping.objects.filter(objecttypeid_id=object_type,masterobject='Y')
			if unique_master:
				unique_master = True
			else:
				unique_master = False
			groupingrequired = objecttypemaster.groupingrequired
			if groupingrequired =='Y'and unique_master == False:
				response["status"]=True
			else:
				response["status"]=False

			obj_master_records = Objectsensormapping.objects.filter(objecttypeid_id=object_type)
			groupcount = objecttypemaster.groupcount
			if  len(obj_master_records) == groupcount:
				response["record_status"] =False
			else:
				response["record_status"] =True
				
			return HttpResponse(json.dumps(response),content_type="application/json")
		masterobject = request.POST.get("masterobject")
		if masterobject != 'Y':
			masterobject = 'N'
		try:
			objectsensormapping=Objectsensormapping(
				objectname=objectname,
				workflowid_id=workflow,
				sensorid_id=sensor,
				companyid_id=companyid,
				objecttypeid_id=objecttype,
				activerecord=activerecord,
				masterobject = masterobject,
			)
			objectsensormapping.save()
		
		except Exception as e:
			pass
		return HttpResponseRedirect('/object-sensor-mapping')

class UpdateObjectSensorMapping(TemplateView):
	template_name='update_object_sensor_mapping.html'
	def get(self,request,*args,**kwargs):
		try:
			company=Companymaster.objects.filter(activecompany='Y')
			object_id=kwargs.get('object_id')
			workflow=Workflowmaster.objects.all()
			sensor=Sensormaster.objects.all()
			objecttype=Objecttypemaster.objects.all()
			data=Objectsensormapping.objects.get(objectid=object_id)

			if 'username' in request.session:
				user= request.session['username']
				user_obj=Usermaster.objects.get(username=user)
				companyid=user_obj.companyid.companyid
				try:
					company=Companymaster.objects.get(companyid=companyid)
					sensor=Sensormaster.objects.filter(companyid_id=companyid)
					workflow=Workflowmaster.objects.filter(companyid_id=companyid)
				except Exception as e:
					pass

		except Exception as e:
			pass
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			objectid=request.POST.get('objectid')
			objsensormap_obj=Objectsensormapping.objects.get(objectid=objectid)
			objsensormap_obj.objectname=request.POST.get('objectname')	
			objsensormap_obj.companyid_id=request.POST.get('selectedcompany')
			objsensormap_obj.sensorid_id=request.POST.get('selectedsensor')
			objsensormap_obj.workflowid_id=request.POST.get('selectedworkflow')
			objsensormap_obj.objecttypeid_id=request.POST.get('selectedobjecttype')
			objsensormap_obj.activerecord=request.POST.get('activerecord')
			objsensormap_obj.save()	
		except Exception as e:
			pass 
		return HttpResponseRedirect('/object-sensor-mapping')

class DeleteObjectsensormap(View):
	def post(self, request, *args, **kwargs):
		response = {}
		object_id = request.POST.get("id")
		try:
			Objectsensormapping.objects.get(objectid=object_id).delete()
			response["status"]=True
		except Exception as e:
			pass
			response["status"]=False
		return HttpResponse(json.dumps(response),content_type="application/json")

class Transaction(TemplateView):
	template_name='object_transaction.html'
	
	def get(self,request,*args,**kwargs):
		current=datetime.datetime.today().date()
		currentdate=datetime.datetime.strftime(current, '%Y-%m-%d')
		zones = Objecttransaction.objects.values("zonename").distinct()
		sensors = Objecttransaction.objects.values("sensorid").distinct()
		objecttypes = Objecttypemaster.objects.values("objecttypeid","objecttypename").distinct()

		current=datetime.datetime.today().date()
		currentdate=datetime.datetime.strftime(current, '%Y-%m-%d')
		
		query_list = []
		fromdate = request.GET.get("fromdate")
		todate = request.GET.get("todate")
		filter_zone_name = request.GET.get("zonename")
		filter_sensor_id = request.GET.get("sensorid")
		filter_object_type = request.GET.get("objecttype")
		try:

			if fromdate and todate:
				query_list.append(Q(entrydatetime__range=[fromdate, todate]))
			if filter_zone_name:
				query_list.append(Q(zonename=filter_zone_name))
			if filter_sensor_id:
				query_list.append(Q(sensorid=filter_sensor_id))
			if filter_object_type:
				query_list.append(Q(objecttypeid_id=filter_object_type))

			if query_list:
				transactions1 = Objecttransaction.objects.filter(reduce(operator.and_, query_list)).order_by('-entrydatetime')
			else:
				transactions1 = Objecttransaction.objects.filter(zonename__isnull=False).order_by('-entrydatetime')
			print("transactions1>>>",transactions1.count())
			page = request.GET.get('page', 1)
			paginator = Paginator(transactions1, 100)
			try:
				transactions = paginator.page(page)
			except PageNotAnInteger:
				transactions = paginator.page(1)
			except EmptyPage:
				transactions = paginator.page(paginator.num_pages)
		except Exception as e:
			raise e
		return render(request,self.template_name,locals())

	



class AddObjectTypeView(TemplateView):
	template_name = 'add_object_type.html'

	def post(self,request,*args,**kwargs):
		objecttypename = request.POST.get("objecttypename")
		companyid = request.POST.get("companyid")
		movingobject = request.POST.get("movingobject")
		groupingrequired = request.POST.get("groupingrequired")
		groupcount = request.POST.get("groupcount")
		if movingobject  != 'Y':
			movingobject = 'N'
		if groupingrequired != 'Y':
			groupingrequired = 'N'
		if groupcount == '':
			groupcount = 0
		objecttype_obj = Objecttypemaster(
			objecttypename = objecttypename,
			companyid = int(companyid),
			movingobject = movingobject,
			groupingrequired = groupingrequired,
			groupcount = groupcount,

			)
		objecttype_obj.save()
		return HttpResponseRedirect('/object-types')

class ObjectTypes(TemplateView):
	template_name = 'object_types.html'
	def get(self,request,*args,**kwargs):
		objecttypes = Objecttypemaster.objects.all().order_by('-objecttypeid')
		if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				objecttypes = Objecttypemaster.objects.filter(companyid=companyid).order_by('-objecttypeid')
		
		return render(request,self.template_name,locals())

class EditObjectType(TemplateView):
	template_name='edit_object_type.html'
	def get(self,request,*args,**kwargs):
		object_type_id=kwargs.get('object_type_id')
		data=Objecttypemaster.objects.get(objecttypeid=object_type_id)
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		try:
			object_type_id=kwargs.get('object_type_id')
			object_type_obj=Objecttypemaster.objects.get(objecttypeid=object_type_id)
			object_type_obj.objecttypename = request.POST.get("objecttypename")
			object_type_obj.companyid = request.POST.get("companyid")
			object_type_obj.movingobject = request.POST.get("movingobject")
			object_type_obj.groupingrequired = request.POST.get("groupingrequired")
			object_type_obj.groupcount = request.POST.get("groupcount")
			if object_type_obj.movingobject  != 'Y':
				object_type_obj.movingobject = 'N'
			if object_type_obj.groupingrequired != 'Y':
				object_type_obj.groupingrequired = 'N'
			if object_type_obj.groupcount == '':
				object_type_obj.groupcount = 0

			object_type_obj.save()
		except Exception as e:
			raise e
		return HttpResponseRedirect('/object-types')

class Detail(TemplateView):
	template_name='object_detail.html'

	def get(self,request,*args,**kwargs):
		current=datetime.datetime.today().date()
		currentdate=datetime.datetime.strftime(current, '%Y-%m-%d')
		datetime_current = datetime.datetime.now(timezone.utc)
		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				details=Objectzonedetails.objects.filter(companyid=companyid)
				zones = Objectzonedetails.objects.filter(companyid=companyid).values("zonename").distinct()
				sensor_id = Objectzonedetails.objects.filter(companyid=companyid).values("sensorid").distinct()
				object_types = Objecttypemaster.objects.filter(companyid=companyid).values("objecttypeid","objecttypename").distinct()
			else:
				details=Objectzonedetails.objects.all()
				dict_zonechange ={}
				for value in details:
					if value.zoneentrydatetime != None:
						duration = datetime_current-value.zoneentrydatetime
						duration_in_s = duration.total_seconds()
						minutes_zonechange = divmod(duration_in_s, 60)[0]
						objectid=value.objectid.objectid
						dict_zonechange[objectid]=minutes_zonechange
				
				object_types = Objecttypemaster.objects.values("objecttypeid","objecttypename").distinct()
				zones = Objectzonedetails.objects.values("zonename").distinct()
				sensor_id = Objectzonedetails.objects.values("sensorid").distinct()
				
		except Exception as e:
			raise e
		return render(request,self.template_name,locals())

	



class FilterDetailData(View):

	def get(self,request,*args,**kwargs):
		response={}
		current=datetime.datetime.today().date()
		currentdate=datetime.datetime.strftime(current, '%Y-%m-%d')
		datetime_current = datetime.datetime.now(timezone.utc)
		fromdate = request.GET.get("from")
		todate = request.GET.get("to")
		filter_zone = request.GET.get("filter_zone")
		filter_sensor_id = request.GET.get("filter_sensor_id")
		filter_object_type = request.GET.get("filter_object_type")
		radio_filter = request.GET.get("active")
		details_list=[]
		query_list = []
		try:
			if 'username' in request.session:
				user= request.session['username']
				active_user_info=Usermaster.objects.get(username=user)
				companyid=active_user_info.companyid.companyid
				details=Objectzonedetails.objects.filter(companyid=companyid)
				zones = Objectzonedetails.objects.filter(companyid=companyid).values("zonename").distinct()
				sensor_id = Objectzonedetails.objects.filter(companyid=companyid).values("sensorid").distinct()
				object_types = Objecttypemaster.objects.filter(companyid=companyid).values("objecttypeid","objecttypename").distinct()

				if fromdate and todate:
					query_list.append(Q(updateddatetime__range=[fromdate, todate],companyid=companyid))
				if filter_zone:
					query_list.append(Q(zonename=filter_zone,companyid=companyid))
				if filter_sensor_id:
					query_list.append(Q(sensorid=filter_sensor_id,companyid=companyid))
				if filter_object_type:
					query_list.append(Q(objecttypeid_id=filter_object_type,companyid=companyid))
				if radio_filter and radio_filter == 'Y':
					query_list.append(Q(activerecord='Y',companyid=companyid))
				if radio_filter and radio_filter == 'N':
					query_list.append(Q(activerecord='N',companyid=companyid))

				if query_list:
					details = Objectzonedetails.objects.filter(reduce(operator.and_, query_list))
				else:
						details = Objectzonedetails.objects.filter(companyid=companyid)		
			else:
				object_types = Objecttypemaster.objects.values("objecttypeid","objecttypename").distinct()
				zones = Objectzonedetails.objects.values("zonename").distinct()
				sensor_id = Objectzonedetails.objects.values("sensorid").distinct()

				if fromdate and todate:
					query_list.append(Q(updateddatetime__range=[fromdate, todate]))
				if filter_zone:
					query_list.append(Q(zonename=filter_zone))
				if filter_sensor_id:
					query_list.append(Q(sensorid=filter_sensor_id))
				if filter_object_type:
					query_list.append(Q(objecttypeid_id=filter_object_type))
				if radio_filter and radio_filter == 'Y':
					query_list.append(Q(activerecord='Y'))
				if radio_filter and radio_filter == 'N':
					query_list.append(Q(activerecord='N'))

				if query_list:
					details = Objectzonedetails.objects.filter(reduce(operator.and_, query_list))
				else:
						details = Objectzonedetails.objects.all()

				
			minutes_zonechange = ''

			for data in details:
				updateddatetime=datetime.datetime.strftime(data.updateddatetime, '%Y-%m-%d')

				if data.zoneentrydatetime != None:
						duration = datetime_current-data.zoneentrydatetime
						duration_in_s = duration.total_seconds()
						minutes_zonechange = divmod(duration_in_s, 60)[0]
				details_dict={
				'zonename':data.zonename,
				'sensorid':data.sensorid,
				'objectname':data.objectname,
				'objecttype':data.objecttypeid.objecttypename,
				'paramvalues':data.paramvalues,
				'dashboardlink':data.dashboardlink,
				'updateddatetime':updateddatetime,
				'timesincezonecahnge':minutes_zonechange
				}
				details_list.append(details_dict) 

			if details_list:
				response['response_data']=details_list
				response['status']=True
			else:
				response['status']=False

		except Exception as e:
			response['status']=False
			raise e
		return HttpResponse(json.dumps(response),content_type="application/json")
		