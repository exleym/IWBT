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
    short_description = models.CharField(max_length=128, blank=True)
    difficulty = models.CharField(max_length=16)
    max_diff = models.IntegerField(blank=True)
    gauge_id = models.ForeignKey(Gauge, blank=True)

    def __unicode__(self):
        return self.river_name + ' - ' + self.section_name

    def get_url(self):
        return self.river_name.lower().replace(' ', '') + '/' + self.section_name.lower().replace(' ', '')

class Rapid(models.Model):
    river_id = models.ForeignKey(River)
    rapid_name = models.CharField(max_length=64)
    difficulty = models.CharField(max_length=16, blank=True)
    rapid_lat = models.FloatField(blank=True)
    rapid_lon = models.FloatField(blank=True)

    def __unicode__(self):
        return self.rapid_name


class Trip(models.Model):
    user_id = models.ForeignKey(User)
    river_id = models.ForeignKey(River)
    create_date = models.DateField()
    paddle_date = models.DateField()
    flow = models.FloatField(blank=True)
    level = models.FloatField(blank=True)
    swim_count = models.IntegerField()

    def __unicode__(self):
        return self.user_id.user_name + ": " + self.river_id.river_name + " - " + self.paddle_date.strftime('%m/%d/%Y')

    def get_flows_from_usgs(self):
        gauge = self.river_id.gauge_id


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
