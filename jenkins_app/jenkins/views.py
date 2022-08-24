import json
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from jenkins.models import Developer
from jenkins.version import d
from .build_info import create_build_info
# Create your views here.

class CreateUser(APIView):
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            jenkins_username = request.data.get('jenkins_username')
            build_token = request.data.get('build_token')
            Developer.objects.create(username=username,password=make_password(password),jenkins_username=jenkins_username,build_token=build_token)
        except Exception as e:
            data = {'error':"Error in creating User"}    
            return JsonResponse(data=data,status=400)
        return JsonResponse(data={'success':"User Created Successfully"},status=200)
    
class LoginUser(APIView):
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            a = Developer.objects.filter(username=username).first()
            if a and check_password(password,a.password):
                data = {'username':a.username,'jenkins_username':a.jenkins_username,'build_token':a.build_token}
                return JsonResponse(data=data,status=200)
            else:
                return JsonResponse(data={'error':'username or password incorrect'},status=400)
            
        except Exception as e:
            print(e)
            return JsonResponse(data={'error':'Error in getting response'},status=500)
        
    def get(self,request):
        return JsonResponse(data={'success':"ok"},status=200)
    
class VersionInfo(APIView):
    def get(self,request):
        return JsonResponse(data=d,status=200,safe=False)
    
    
class Build_Current_Info(APIView):
    def get(self,request):
        try:
            username = request.data.get('username')
            a = Developer.objects.filter(username=username).first()
            build_data = create_build_info().call_jenkins(a.jenkins_username,a.build_token)
#             build_data = {
# 	'mfapplication': [{
# 		'is_building': True,
# 		'server': 'QA',
# 		'user': 'mayurkulkarni',
# 		'build_result': 'None',
# 		'build_time': '2022-08-23 10:15:08',
# 		'estimatedDuration': 267,
# 		'build_estimate': 2,
# 		'percent_value': 90
# 	}],
# 	'build_cnt': 0,
# 	'mfadmin': [{
# 		'is_building': True,
# 		'server': 'UAT',
# 		'user': 'vishaldhande',
# 		'build_result': 'None',
# 		'build_time': '2022-08-22 18:25:23',
# 		'estimatedDuration': 270,
# 		'build_estimate': 3,
# 		'percent_value': 90
# 	}],
# 	'mfcronicle': [{
# 		'is_building': False,
# 		'server': 'http://bitbucket.bfsgodirect.com/scm/bfdlmf/mfcore.git',
# 		'user': 'mayurkulkarni',
# 		'build_result': 'SUCCESS',
# 		'build_time': '2022-08-23 09:51:18',
# 		'estimatedDuration': 102,
# 		'build_duration': 93024,
# 		'percent_value': 0.0
# 	}],
# 	'mfconsumer': [{
# 		'is_building': False,
# 		'server': 'UAT',
# 		'user': 'vishaldhande',
# 		'build_result': 'SUCCESS',
# 		'build_time': '2022-08-22 18:51:42',
# 		'estimatedDuration': 347,
# 		'build_duration': 280914,
# 		'percent_value': 0.0
# 	}]
# }         
            print(build_data)
            return JsonResponse(data=build_data,status=200)
        except:
            build_data = {"error":"error in getting data"}
            return JsonResponse(data=build_data,status=400)