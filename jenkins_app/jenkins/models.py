from django.db import models

# Create your models here.

class Developer(models.Model):
    developer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,blank=False,null=False,unique=True)
    password = models.CharField(max_length=500,blank=False,null=False)
    build_token = models.CharField(max_length=100,blank=True,null=True)
    jenkins_username = models.CharField(max_length=50,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)