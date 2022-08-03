from django.urls import path
from .views import *

urlpatterns = [
    path('addVendor', add_vendor, name='add_vendor'),
    path('addPhoneNumber', add_phone_number, name='add_phone_number'),
]
