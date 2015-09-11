from django.db import models

# Create your models here.
class Gauge(models.Model):
	usgs_id = models.CharField(max_length=32)

	def __unicode__(self):
		return self.usgs_id


class User(models.Model):
	user_name = models.CharField(max_length=32)
	create_date = models.DateField()
	# pw_salt = models.CharField(max_length=16)
	# pw_hashed = models.CharField(max_length=128)

	def __unicode__(self):
		return self.user_name


class River(models.Model):
	river_name = models.CharField(max_length=64)
	section_name = models.CharField(max_length=64)
	difficulty = models.CharField(max_length=16)
	max_diff = models.IntegerField()
	gauge_id = models.ForeignKey(Gauge)

	def __unicode__(self):
		return self.river_name + ' - ' + self.section_name


class Trip(models.Model):
	user_id = models.ForeignKey(User)
	river_id = models.ForeignKey(River)
	create_date = models.DateField()
	paddle_date = models.DateField()
	flow = models.FloatField()
	level = models.FloatField()
	swim_count = models.IntegerField()

	def swam(self):
		return self.swim_count > 0


class TripKey(models.Model):
	key_name = models.CharField(max_length=64)


class TripVarData(models.Model):
	trip_id = models.ForeignKey(Trip)
	key = models.ForeignKey(TripKey)
	value = models.CharField(max_length=128)


class GaugeData(models.Model):
	gauge_id = models.ForeignKey(Gauge)
	timestamp = models.DateTimeField()
	flow_level = models.FloatField()
	gauge_level = models.FloatField()
