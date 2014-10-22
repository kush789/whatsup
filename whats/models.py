from django.db import models

# Create your models here.


class usersinfo(models.Model):
	uid = models.AutoField(primary_key = True)
	loginid = models.CharField(max_length = 50, unique = True)
	role = models.IntegerField(default = 1)		#user - >1 admin ->9
	status = models.IntegerField(default = 1)	#active -> 1 inactive -> 0
	fname = models.CharField(default = "", max_length = 30)
	lname = models.CharField(default = "", max_length = 30)
	number = models.IntegerField(max_length = 20)


class posts(models.Model):
	pid = models.AutoField(primary_key = True)
	uid = models.IntegerField(max_length = 15)
	fname = models.CharField(max_length = 50)
	lname = models.CharField(max_length = 50)
	title = models.CharField(max_length = 50)
	loginid = models.CharField(max_length = 50)
	posttext = models.CharField(max_length = 300, default = "")
	upcount = models.IntegerField(max_length = 15, default = 0)
	downcount = models.IntegerField(max_length = 15, default = 0)
	postimage = models.ImageField(upload_to="postimg/")
	timestamp = models.DateTimeField(auto_now = True)

class comments(models.Model):
	cid = models.AutoField(primary_key = True)
	uid = models.IntegerField(max_length = 15)
	pid = models.IntegerField(max_length = 15)
	fname = models.CharField(max_length = 50)
	lname = models.CharField(max_length = 50)
	loginid = models.CharField(max_length = 50)
	commenttext = models.CharField(max_length = 300, default = "")
	upcount = models.IntegerField(max_length = 15, default = 0)
	downcount = models.IntegerField(max_length = 15, default = 0)
	timestamp = models.DateTimeField(auto_now = True)

