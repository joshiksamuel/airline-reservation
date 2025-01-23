from django.contrib import admin
from flight.models import *
# Register your models here.
admin.site.register(Flight)
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Contact)
admin.site.register(Payment)