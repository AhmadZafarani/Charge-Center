from django.urls import path
from .views import *

urlpatterns = [
    path('addVendor', add_vendor, name='add_vendor'),
]
