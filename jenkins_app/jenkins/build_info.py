
from datetime import timedelta
import requests
import os
import time
import datetime

# url = 'https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MFApplicationService/lastBuild/api/json'
# url = 'https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MFApplicationService/lastBuild/api/json'
# url = 'https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MFApplicationService/lastBuild/api/json'
# url = 'https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MFApplicationService/lastBuild/api/json'


# response = requests.post(url, auth=(os.environ['build_username'], os.environ['build_token']))
# print(response.json()['building'])
# print(response.json()['actions'][0]['parameters'][2]['value'])
# print(response.json()['actions'][1]['causes'][0]['userId'])
# print(response.json()['result'])
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(response.json()['timestamp'])[:-3]))))
# print(response.json()['estimatedDuration'])
# print(response.json()['duration'])

class create_build_info():
    def __init__(self):
      self.urls = ['https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MFApplicationService/lastBuild/api/json',
                    'https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MFAdminService/lastBuild/api/json',
                    'https://jenkins-nprd.bfsgodirect.com/job/Pipeline-MF-CronicleWorker/lastBuild/api/json',
                    'https://jenkins-nprd.bfsgodirect.com/job/Python-Pipeline-mfconsumerservice/lastBuild/api/json',]
      
      self.job_name = ['mfapplication','mfadmin','mfcronicle','mfconsumer']
      
    def call_jenkins(self,username,build_token):
        data = {}
        cnt = 0
        if username and build_token:
            for index,url in enumerate(self.urls):
                data[self.job_name[index]] = []
                response = requests.post(url, auth=(os.environ['build_username'], os.environ['build_token']))
                response = response.json()
                build_no = response['number']
                print(build_no,response['nextBuild'],response['previousBuild'])
                self.new_method(data, cnt, index, response)
                if response['nextBuild']:
                    url = url.replace('lastBuild',str(response['nextBuild']['number']))
                    response = requests.post(url, auth=(os.environ['build_username'], os.environ['build_token']))
                    response = response.json()
                    if response['building']:
                        self.new_method(data, cnt, index, response)
                if response['previousBuild']:
                    url = url.replace('lastBuild',str(response['previousBuild']['number']))
                    response = requests.post(url, auth=(os.environ['build_username'], os.environ['build_token']))
                    response = response.json()
                    if response['building']:
                        self.new_method(data, cnt, index, response)
                data['build_cnt'] = cnt
        return data

    def new_method(self, data, cnt, index, response):
        is_building = response['building']
        server = response['actions'][0]['parameters'][1]['value'] if index==2 else response['actions'][0]['parameters'][2]['value']
        user = response['actions'][1]['causes'][0]['userId']
        build_result = response['result']
        build_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(response['timestamp'])[:-3])))
        build_time = datetime.datetime.strptime(build_time,'%Y-%m-%d %H:%M:%S')
        build_time_datetime = build_time - timedelta(minutes=7.5)
        build_time = datetime.datetime.strftime(build_time_datetime,'%Y-%m-%d %H:%M:%S')
        estimatedDuration = int(response['estimatedDuration']/1000)
        build_duration = response['duration']
        build_estimate = 1
        if is_building == True:
            # if datetime.datetime.now() < build_time_datetime:
            # build_time_datetime = datetime.datetime.now()
            total_sec = (datetime.datetime.now() - build_time_datetime).total_seconds()
            print(total_sec)
            if total_sec >=estimatedDuration:
                percent_value = 99
            else:
                percent_value = int(total_sec/estimatedDuration*100)
            cnt+=1
            build_estimate = estimatedDuration-total_sec/(100-percent_value) if total_sec < estimatedDuration else 1
        else:
            percent_value = 0
                
        print(is_building)
        data[self.job_name[index]].append({
            'is_building':is_building,
                'server':server,
                'user':user,
                'build_result':build_result,
                'build_time':build_time,
                'estimatedDuration':estimatedDuration,
                'build_estimate':build_estimate,
                'percent_value':percent_value
            })
        return data
    
        
# print(create_build_info().call_jenkins())