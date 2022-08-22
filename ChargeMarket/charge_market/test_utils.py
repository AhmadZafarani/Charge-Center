from random import randint

from django.test import TestCase

from .models import ChargeTransaction, PhoneNumber, SellTransaction, Vendor


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
    test_case_obj.assertEqual(ChargeTransaction.objects.count(), identifier)
    transaction = ChargeTransaction.objects.all()[identifier - 1]
    test_case_obj.assertEqual(transaction.identifier, identifier)
    test_case_obj.assertEqual(transaction.amount, charge)
    test_case_obj.assertEqual(transaction.vendor, vendor)
    vendor.refresh_from_db()
    test_case_obj.assertEqual(vendor.get_credit(), first_credit + charge)


def add_phone_number(test_case_obj: TestCase, index: int, phone_number_value: str) -> PhoneNumber:
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
    test_case_obj.assertEqual(SellTransaction.objects.count(), identifier)
    transaction = SellTransaction.objects.all()[identifier - 1]
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
                                 phone_number: PhoneNumber, charge: int = 10):
    response = test_case_obj.client.post(
        '/sell-charge', {"vendor_id": f"{vendor_id}", "phone_number": phone_number.phone_number,
                         "charge": f"{charge}"})
    test_case_obj.assertEqual(response.status_code, 400)
    test_case_obj.assertEqual(response.content.decode(
        "utf-8"), "not enough credit to sell this charge")


def add_vendors(test_case_obj: TestCase, count: int) -> list:
    vendors = []
    for i in range(1, count):
        first_credit = randint(0, 100)
        vendor = add_vendor(test_case_obj, i, first_credit)
        vendors.append(vendor)
    return vendors


def add_phone_numbers(test_case_obj: TestCase, count: int) -> list:
    phone_numbers = []
    for i in range(1, count):
        phone_number_value = f'0935629245{i}'
        phone_number = add_phone_number(test_case_obj, i, phone_number_value)
        phone_numbers.append(phone_number)
    return phone_numbers


def increase_vendor_credit_randomly(test_case_obj: TestCase, vendor: Vendor, transaction_identifier: int, vendor_transactions_dict: dict) -> int:
    transaction_identifier += 1
    charge = randint(101, 1000)
    increase_vendor_credit(
        test_case_obj, transaction_identifier, vendor.identifier, charge, vendor.get_credit(), vendor)
    transactions = vendor_transactions_dict[vendor]
    transactions.append(charge)
    return transaction_identifier
