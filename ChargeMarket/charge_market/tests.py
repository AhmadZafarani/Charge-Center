from django.db import IntegrityError
from django.db.transaction import atomic
from django.forms import ValidationError
from django.test import TestCase

from .models import *
from .test_utils import *


class VendorModelTest(TestCase):
    def test_string_representation(self):
        vendor = Vendor()
        vendor.identifier = 1
        vendor.set_credit(200)
        self.assertEqual(str(vendor), f"vendor with id: 1 and credit: 200")


class AddVendorTests(TestCase):
    def test_empty_arguments(self):
        response = self.client.get('/add-vendor')
        self.assertEqual(response.status_code, 400)

    def test_add_vendor(self):
        add_vendor(self, 1, 21)

    def test_add_multiple_vendors(self):
        add_vendor(self, 1, 21)
        add_vendor(self, 2, 25)

    def test_add_vendor_negative_credit(self):
        with atomic():
            response = self.client.get('/add-vendor?credit=-21')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_add_vendor_zero_credit(self):
        add_vendor(self, 1, 0)

    def test_add_vendor_float_credit(self):
        with atomic():
            response = self.client.get('/add-vendor?credit=1.2')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 0)


class AddPhoneNumberTests(TestCase):
    def test_empty_arguments(self):
        response = self.client.get('/add-phone-number')
        self.assertEqual(response.status_code, 400)

    def test_add_phone_number(self):
        index = 1
        phone_number = '09356292458'
        add_phone_number(self, index, phone_number)

    def test_add_multiple_phone_numbers(self):
        index = 1
        phone_number = '09356292458'
        add_phone_number(self, index, phone_number)

        index = 2
        phone_number = '09356292457'
        add_phone_number(self, index, phone_number)

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


class IncreaseVendorCreditTests(TestCase):
    def test_empty_arguments(self):
        response = self.client.post('/increase-credit')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(
            "utf-8"), "vendor_id not found!")

        response = self.client.post('/increase-credit', {"vendor_id": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"), "charge not found!")

        response = self.client.post('/increase-credit', {"charge": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(
            "utf-8"), "vendor_id not found!")

    def test_increase_not_existing_vendor_credit(self):
        response = self.client.post(
            '/increase-credit', {"vendor_id": "1", "charge": "200"})
        self.assertEqual(response.status_code, 404)

    def test_increase_vendor_credit(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        increase_vendor_credit(self, 1, vendor_id, 200, first_credit, vendor)

    def test_increase_vendor_credit_multiple_times(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        increase_vendor_credit(self, 1, vendor_id, 200, first_credit, vendor)
        increase_vendor_credit(self, 2, vendor_id, 300,
                               first_credit + 200, vendor)

    def test_increase_multiple_vendors_credit(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        increase_vendor_credit(self, 1, vendor_id, 200, first_credit, vendor)

        vendor_id = 2
        first_credit = 22
        vendor = add_vendor(self, vendor_id, first_credit)
        increase_vendor_credit(self, 2, vendor_id, 300, first_credit, vendor)

    def test_increase_multiple_vendors_credit_multiple_times(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        increase_vendor_credit(self, 1, vendor_id, 200, first_credit, vendor)
        increase_vendor_credit(self, 2, vendor_id, 300,
                               first_credit + 200, vendor)

        vendor_id = 2
        first_credit = 22
        vendor = add_vendor(self, vendor_id, first_credit)
        increase_vendor_credit(self, 3, vendor_id, 400, first_credit, vendor)
        increase_vendor_credit(self, 4, vendor_id, 500,
                               first_credit + 400, vendor)


class SellChargeTests(TestCase):
    def test_empty_arguments(self):
        response = self.client.post('/sell-charge')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(
            "utf-8"), "vendor_id not found!")

        response = self.client.post('/sell-charge', {"vendor_id": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(
            "utf-8"), "phone_number not found!")

        response = self.client.post(
            '/sell-charge', {"vendor_id": "1", "phone_number": "09123456789"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(
            "utf-8"), "charge not found!")

    def test_sell_charge_from_not_existing_vendor(self):
        response = self.client.post(
            '/sell-charge', {"vendor_id": "1", "phone_number": "09123456789",
                             "charge": "200"})
        self.assertEqual(response.status_code, 404)

    def test_sell_charge_to_not_existing_phone_number(self):
        vendor_id = 1
        first_credit = 21
        add_vendor(self, vendor_id, first_credit)
        response = self.client.post(
            '/sell-charge', {"vendor_id": "1", "phone_number": "09123456789",
                             "charge": "200"})
        self.assertEqual(response.status_code, 404)

    def test_sell_charge_more_than_credit(self):
        vendor_id = 1
        first_credit = 21
        add_vendor(self, vendor_id, first_credit)
        index = 1
        phone_number = '09356292458'
        add_phone_number(self, index, phone_number)
        sell_more_than_credit_charge(
            self, vendor_id, phone_number, first_credit+10)

    def test_sell_charge(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        index = 1
        phone_number_value = '09356292458'
        phone_number = add_phone_number(self, index, phone_number_value)
        sell_charge(self, 1, vendor, phone_number, 10, first_credit)

    def one_vendor_sell_charge_to_one_phone_number_multiple_times(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        index = 1
        phone_number_value = '09356292458'
        phone_number = add_phone_number(self, index, phone_number_value)
        sell_charge(self, 1, vendor, phone_number, 10, first_credit)
        sell_charge(self, 2, vendor, phone_number, 10, first_credit-10, 10)
        sell_more_than_credit_charge(self, vendor_id, phone_number)

    def one_vendor_sell_charge_to_multiple_phone_numbers(self):
        vendor_id = 1
        first_credit = 21
        vendor = add_vendor(self, vendor_id, first_credit)
        index = 1
        phone_number_value = '09356292458'
        phone_number = add_phone_number(self, index, phone_number_value)
        sell_charge(self, 1, vendor, phone_number, 10, first_credit)
        index = 2
        phone_number_value = '09356292457'
        phone_number = add_phone_number(self, index, phone_number_value)
        sell_charge(self, 2, vendor, phone_number, 10, first_credit-10)
        index = 2
        phone_number_value = '09356292456'
        phone_number = add_phone_number(self, index, phone_number_value)
        sell_more_than_credit_charge(self, vendor_id, phone_number)

    def multiple_vendors_sell_charge_to_one_phone_number(self):
        vendor_id_1 = 1
        first_credit_1 = 21
        vendor_1 = add_vendor(self, vendor_id_1, first_credit_1)
        vendor_id_2 = 2
        first_credit_2 = 31
        vendor_2 = add_vendor(self, vendor_id_2, first_credit_2)
        index = 1
        phone_number_value = '09356292458'
        phone_number = add_phone_number(self, index, phone_number_value)
        sell_charge(self, 1, vendor_1, phone_number, 10, first_credit_1)
        sell_charge(self, 2, vendor_2, phone_number, 10, first_credit_2, 10)
        sell_charge(self, 3, vendor_1, phone_number, 10, first_credit_1-10, 20)
        sell_charge(self, 4, vendor_2, phone_number, 10, first_credit_2-10, 30)
        sell_more_than_credit_charge(self, vendor_id_1, phone_number)
        sell_charge(self, 5, vendor_2, phone_number, 10, first_credit_2-20, 40)
        sell_more_than_credit_charge(self, vendor_id_2, phone_number)
