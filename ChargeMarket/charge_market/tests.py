from django.test import TestCase

from .models import *


class VendorModelTest(TestCase):
    def test_string_representation(self):
        vendor = Vendor()
        vendor.identifier = 1
        vendor.credit = 200
        self.assertEqual(str(vendor), f"vendor with id: 1 and credit: 200")


class ProjectTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
