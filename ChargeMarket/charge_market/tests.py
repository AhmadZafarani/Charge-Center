from django.db import IntegrityError
from django.db.transaction import atomic
from django.forms import ValidationError
from django.test import TestCase

from .models import *


class VendorModelTest(TestCase):
    def test_string_representation(self):
        vendor = Vendor()
        vendor.identifier = 1
        vendor.credit = 200
        self.assertEqual(str(vendor), f"vendor with id: 1 and credit: 200")


class AddVendorTests(TestCase):
    def test_add_vendor(self):
        response = self.client.get('/addVendor?credit=21')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 1)
        vendor = Vendor.objects.all()[0]
        self.assertEqual(vendor.identifier, 1)
        self.assertEqual(vendor.credit, 21)

    def test_add_multiple_vendors(self):
        response = self.client.get('/addVendor?credit=21')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 1)
        vendor = Vendor.objects.all()[0]
        self.assertEqual(vendor.identifier, 1)
        self.assertEqual(vendor.credit, 21)

        response = self.client.get('/addVendor?credit=25')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 2)
        vendor = Vendor.objects.all()[1]
        self.assertEqual(vendor.identifier, 2)
        self.assertEqual(vendor.credit, 25)

    def test_add_vendor_negative_credit(self):
        with atomic():
            response = self.client.get('/addVendor?credit=-21')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_add_vendor_zero_credit(self):
        response = self.client.get('/addVendor?credit=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 1)
        vendor = Vendor.objects.all()[0]
        self.assertEqual(vendor.identifier, 1)
        self.assertEqual(vendor.credit, 0)

    def test_add_vendor_float_credit(self):
        with atomic():
            response = self.client.get('/addVendor?credit=1.2')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 0)


class AddPhoneNumberTests(TestCase):
    def test_add_phone_number(self):
        response = self.client.get('/addPhoneNumber?phone_number=09356292458')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PhoneNumber.objects.count(), 1)
        phone_number = PhoneNumber.objects.all()[0]
        self.assertEqual(phone_number.phone_number, '09356292458')

    def test_add_multiple_phone_numbers(self):
        response = self.client.get('/addPhoneNumber?phone_number=09356292458')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PhoneNumber.objects.count(), 1)
        phone_number = PhoneNumber.objects.all()[0]
        self.assertEqual(phone_number.phone_number, '09356292458')

        response = self.client.get('/addPhoneNumber?phone_number=09356292457')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PhoneNumber.objects.count(), 2)
        phone_number = PhoneNumber.objects.all()[1]
        self.assertEqual(phone_number.phone_number, '09356292457')

    def test_add_phone_number_multiple_times(self):
        PhoneNumber.objects.create(phone_number='09356292457')
        with self.assertRaises(IntegrityError):
            PhoneNumber.objects.create(phone_number='09356292457')

    def test_add_invalid_phone_number(self):
        phone_number = PhoneNumber.objects.create(phone_number='salam')
        with self.assertRaises(ValidationError):
            phone_number.full_clean()

        phone_number = PhoneNumber.objects.create(phone_number='1234567890')
        with self.assertRaises(ValidationError):
            phone_number.full_clean()

        phone_number = PhoneNumber.objects.create(phone_number='091234567890')
        with self.assertRaises(ValidationError):
            phone_number.full_clean()
