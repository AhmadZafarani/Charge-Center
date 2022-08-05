from django.test import TestCase

from .models import Vendor


def add_vendor(add_vendor_tests: TestCase, identifier: int, credit: int) -> Vendor:
    response = add_vendor_tests.client.get(f'/add-vendor?credit={credit}')
    add_vendor_tests.assertEqual(response.status_code, 200)
    add_vendor_tests.assertEqual(Vendor.objects.count(), identifier)
    vendor = Vendor.objects.all()[identifier - 1]
    add_vendor_tests.assertEqual(vendor.identifier, identifier)
    add_vendor_tests.assertEqual(vendor.get_credit(), credit)
    return vendor
