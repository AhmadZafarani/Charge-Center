import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.utils import DataError
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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
    except (IntegrityError, DataError):
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
        phone_number.full_clean()
    except (IntegrityError, ValidationError):
        return HttpResponseBadRequest(error_string)
    phone_number.save()

    success_message = f"{phone_number} created successfully!"
    logger.info(success_message)
    return HttpResponse(success_message)


@csrf_exempt
def increase_credit(request: HttpRequest) -> HttpResponse:
    vendor_id = request.POST.get("vendor_id")
    if vendor_id is None:
        return HttpResponseBadRequest("vendor_id not found!")
    charge = request.POST.get("charge")
    if charge is None:
        return HttpResponseBadRequest("charge not found!")

    vendor = get_object_or_404(Vendor, pk=vendor_id)
    response = ChargeTransaction.save_model(vendor, charge)
    if response is not None:
        return response

    success_message = f"credit of {vendor} increased successfully {charge}$!"
    logger.info(success_message)
    return HttpResponse(success_message)


@csrf_exempt
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
    response = SellTransaction.save_model(vendor, phone_number, charge)
    if response is not None:
        return response

    success_message = f"{vendor} sold {charge}$ charge to {phone_number}  successfully!"
    logger.info(success_message)
    return HttpResponse(success_message)
