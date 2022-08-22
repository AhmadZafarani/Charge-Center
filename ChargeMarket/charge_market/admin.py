from django.contrib import admin

from .models import *

admin.site.register(Vendor)
admin.site.register(PhoneNumber)
admin.site.register(SellTransaction)
admin.site.register(ChargeTransaction)
