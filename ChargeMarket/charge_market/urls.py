from django.urls import path
from .views import *

urlpatterns = [
    path('add-vendor', add_vendor, name='add_vendor'),
    path('add-phone-number', add_phone_number, name='add_phone_number'),
    path('increase-credit', increase_credit, name='increase_credit'),
]
