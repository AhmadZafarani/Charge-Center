from django.test import TestCase

from .models import PhoneNumber, Transaction, Vendor


def add_vendor(test_case_obj: TestCase, identifier: int, credit: int) -> Vendor:
    response = test_case_obj.client.get(f'/add-vendor?credit={credit}')
    test_case_obj.assertEqual(response.status_code, 200)
    test_case_obj.assertEqual(Vendor.objects.count(), identifier)
    vendor = Vendor.objects.all()[identifier - 1]
    test_case_obj.assertEqual(vendor.identifier, identifier)
    test_case_obj.assertEqual(vendor.get_credit(), credit)
    return vendor


def increase_vendor_credit(test_case_obj: TestCase, identifier: int, vendor_id: int,
                           charge: int, first_credit: int, vendor: Vendor):
    response = test_case_obj.client.post(
        '/increase-credit', {"vendor_id": f"{vendor_id}", "charge": f"{charge}"})
    test_case_obj.assertEqual(response.status_code, 200)
    test_case_obj.assertEqual(Transaction.objects.count(), identifier)
    transaction = Transaction.objects.all()[identifier - 1]
    test_case_obj.assertEqual(transaction.identifier, identifier)
    test_case_obj.assertEqual(transaction.amount, charge)
    test_case_obj.assertEqual(transaction.vendor, vendor)
    vendor.refresh_from_db()
    test_case_obj.assertEqual(vendor.get_credit(), first_credit + charge)


def add_phone_number(test_case_obj: TestCase, index: int, phone_number_value: str)\
        -> PhoneNumber:
    response = test_case_obj.client.get(
        f'/add-phone-number?phone_number={phone_number_value}')
    test_case_obj.assertEqual(response.status_code, 200)
    test_case_obj.assertEqual(PhoneNumber.objects.count(), index)
    phone_number = PhoneNumber.objects.all()[index - 1]
    test_case_obj.assertEqual(
        phone_number.phone_number, phone_number_value)
    return phone_number


def sell_charge(test_case_obj: TestCase, identifier: int, vendor: Vendor,
                phone_number: PhoneNumber, charge: int, vendor_first_credit: int,
                phone_number_first_charge: int = 0):
    response = test_case_obj.client.post(
        '/sell-charge', {"vendor_id": f"{vendor.identifier}", "phone_number":
                         phone_number.phone_number, "charge": f"{charge}"})
    test_case_obj.assertEqual(response.status_code, 200)
    test_case_obj.assertEqual(Transaction.objects.count(), identifier)
    transaction = Transaction.objects.all()[identifier - 1]
    test_case_obj.assertEqual(transaction.identifier, identifier)
    test_case_obj.assertEqual(transaction.amount, charge)
    test_case_obj.assertEqual(transaction.vendor, vendor)
    vendor.refresh_from_db()
    test_case_obj.assertEqual(
        vendor.get_credit(), vendor_first_credit - charge)
    phone_number.refresh_from_db()
    test_case_obj.assertEqual(
        phone_number.charge, phone_number_first_charge + charge)


def sell_more_than_credit_charge(test_case_obj: TestCase, vendor_id: int,
                                 phone_number: str, charge: int = 10):
    response = test_case_obj.client.post(
        '/sell-charge', {"vendor_id": f"{vendor_id}", "phone_number": phone_number,
                         "charge": f"{charge}"})
    test_case_obj.assertEqual(response.status_code, 400)
    test_case_obj.assertEqual(response.content.decode(
        "utf-8"), "not enough credit to sell this charge")
