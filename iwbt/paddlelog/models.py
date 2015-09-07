from django.db import models

# Create your models here.

class Trips(models.Model):
	user_id = models.ForeignKey(Users)
	river_id = models.ForeignKey(Rivers)
	create_date = models.DateField()
	paddle_date = models.DateField()
	
class User(models.Model):
	user_name = models.CharField(max_length=32)
	create_date = models.DateField()
	pw_salt = models.CharField(max_length=16)
	pw_hashed = models.CharField(max_length=128)
