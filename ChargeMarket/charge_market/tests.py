from django.test import TestCase

from .models import *


class VendorModelTest(TestCase):
    def test_string_representation(self):
        vendor = Vendor()
        vendor.identifier = 1
        vendor.credit = 200
        self.assertEqual(str(vendor), f"vendor with id: 1 and credit: 200")
