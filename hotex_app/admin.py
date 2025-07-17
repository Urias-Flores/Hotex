from django.contrib import admin
from hotex_app.models import *

# Register your models here.
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Maintenance)