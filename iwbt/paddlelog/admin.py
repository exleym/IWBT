
from django.contrib import admin
import paddlelog.models as dbmodels

admin.site.register(dbmodels.Gauge)
admin.site.register(dbmodels.User)
admin.site.register(dbmodels.River)
admin.site.register(dbmodels.Trip)
