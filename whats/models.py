from django.db import models

# Create your models here.


class userinfo(models.Model):
	uid = models.AutoField(primary_key = True)
	loginid = models.CharField(max_length = 50, unique = True)
	role = models.IntegerField(default = 1)		#user - >1 admin ->9
	status = models.IntegerField(default = 1)	#active -> 1 inactive -> 0
	fname = models.CharField(default = "", max_length = 30)
	lname = models.CharField(default = "", max_length = 30)
	number = models.IntegerField(max_length = 12)
