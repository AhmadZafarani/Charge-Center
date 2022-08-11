import logging

from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import *


logger = logging.getLogger(__name__)


def add_vendor(request: HttpRequest) -> HttpResponse:
    credit = request.GET.get("credit")
    if credit is None:
        return HttpResponseBadRequest("credit not found!")
    vendor = Vendor()
    error_string = "credit must be a positive Integer!"
    try:
        vendor.set_credit(int(credit))
    except ValueError:
        return HttpResponseBadRequest(error_string)
    try:
        vendor.save()
    except IntegrityError:
        return HttpResponseBadRequest(error_string)

    success_message = f"{vendor} created successfully!"
    logger.info(success_message)
    return HttpResponse(success_message)


def add_phone_number(request: HttpRequest) -> HttpResponse:
    phone_number_value = request.GET.get("phone_number")
    if phone_number_value is None:
        return HttpResponseBadRequest("phone_number not found!")
    phone_number = PhoneNumber()
    phone_number.phone_number = phone_number_value
    error_string = "phone number not valid! Example: 09123456789"
    try:
        phone_number.save()
    except IntegrityError:
        return HttpResponseBadRequest(error_string)

    success_message = f"{phone_number} created successfully!"
    logger.info(success_message)
    return HttpResponse(success_message)


def increase_credit(request: HttpRequest) -> HttpResponse:
    vendor_id = request.POST.get("vendor_id")
    if vendor_id is None:
        return HttpResponseBadRequest("vendor_id not found!")
    charge = request.POST.get("charge")
    if charge is None:
        return HttpResponseBadRequest("charge not found!")

    vendor = get_object_or_404(Vendor, pk=vendor_id)
    transaction = ChargeTransaction()
    transaction.vendor = vendor
    try:
        charge = int(charge)
    except ValueError:
        return HttpResponseBadRequest("charge must be a Positive Integer!")

    transaction.amount = charge

    transaction.charge(charge)
    transaction.save()

    success_message = f"credit of {vendor} increased successfully {charge}$!"
    logger.info(success_message)
    return HttpResponse(success_message)


def sell_charge(request: HttpRequest) -> HttpResponse:
    vendor_id = request.POST.get("vendor_id")
    if vendor_id is None:
        return HttpResponseBadRequest("vendor_id not found!")
    phone_number = request.POST.get("phone_number")
    if phone_number is None:
        return HttpResponseBadRequest("phone_number not found!")
    charge = request.POST.get("charge")
    if charge is None:
        return HttpResponseBadRequest("charge not found!")

    vendor = get_object_or_404(Vendor, pk=vendor_id)
    phone_number = get_object_or_404(PhoneNumber, pk=phone_number)
    transaction = SellTransaction()
    transaction.vendor = vendor
    transaction.phone_number = phone_number
    try:
        charge = int(charge)
    except ValueError:
        return HttpResponseBadRequest("charge must be a Positive Integer!")
    transaction.amount = charge

    try:
        transaction.charge(charge)
    except IntegrityError as e:
        return HttpResponseBadRequest(e.with_traceback(None))
    transaction.save()

    success_message = f"{vendor} sold {charge}$ charge to {phone_number}  successfully!"
    logger.info(success_message)
    return HttpResponse(success_message)
