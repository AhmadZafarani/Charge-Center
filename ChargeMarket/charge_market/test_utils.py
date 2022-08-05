from django.test import TestCase

from .models import Transaction, Vendor


def add_vendor(test_case_obj: TestCase, identifier: int, credit: int) -> Vendor:
    response = test_case_obj.client.get(f'/add-vendor?credit={credit}')
    test_case_obj.assertEqual(response.status_code, 200)
    test_case_obj.assertEqual(Vendor.objects.count(), identifier)
    vendor = Vendor.objects.all()[identifier - 1]
    test_case_obj.assertEqual(vendor.identifier, identifier)
    test_case_obj.assertEqual(vendor.get_credit(), credit)
    return vendor


def increase_vendor_credit(test_case_obj: TestCase, identifier: int, vendor_id: int, charge: int, first_credit: int, vendor: Vendor):
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
