from .models import *
def count_objects(request):
	total_companies=''
	total_sensors=''
	total_users=''
	total_zones=''
	try:
		if 'username' in request.session:
			user= request.session['username']
			print("----------USER----------",user)
			active_user_info=Usermaster.objects.get(username=user)
			print('active user',active_user_info)
			companyid=active_user_info.companyid.companyid
			print('companyid',companyid)	
			total_companies=Companymaster.objects.filter(companyid=companyid).count()	
			total_sensors=Sensormaster.objects.filter(companyid=companyid).count()
			total_users=Usermaster.objects.filter(companyid=companyid).count()
			total_zones=Zonemaster.objects.filter(companyid=companyid).count()
		
		elif request.user.is_staff or request.user.is_authenticated:
			total_companies=Companymaster.objects.all().count()	
			total_sensors=Sensormaster.objects.all().count()
			total_users=Usermaster.objects.count()
			total_zones=Zonemaster.objects.all().count()
		return {
		'total_companies':total_companies,
		'total_users':total_users,
		'total_sensors':total_sensors,
		'total_zones':total_zones,
		}
	except Exception as e:
		raise e
