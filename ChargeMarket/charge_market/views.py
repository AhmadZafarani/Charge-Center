from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from .models import *


def add_vendor(request: HttpRequest) -> HttpResponse:
    credit = request.GET.get("credit")
    if credit is None:
        return HttpResponseBadRequest("credit not found!")
    vendor = Vendor()
    error_string = "credit must be a positive Integer!"
    try:
        vendor.credit = int(credit)
    except ValueError:
        return HttpResponseBadRequest(error_string)
    try:
        vendor.save()
    except IntegrityError:
        return HttpResponseBadRequest(error_string)
    return HttpResponse()


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
    return HttpResponse()


def charge(request: HttpRequest) -> HttpResponse:
    vendor_id = request.POST.get("vendor_id")
    if vendor_id is None:
        return HttpResponseBadRequest("vendor_id not found!")
    charge = request.POST.get("charge")
    if charge is None:
        return HttpResponseBadRequest("charge not found!")

    vendor = Vendor.objects.get(identifier=vendor_id)
    if vendor is None:
        return HttpResponseBadRequest("vendor with specified id not found!")

    return HttpResponse()


def increase_credit(request: HttpRequest) -> HttpResponse:
    vendor_id = request.POST.get("vendor_id")
    if vendor_id is None:
        return HttpResponseBadRequest("vendor_id not found!")
    charge = request.POST.get("charge")
    if charge is None:
        return HttpResponseBadRequest("charge not found!")

    vendor = Vendor.objects.get(pk=vendor_id)
    if vendor is None:
        return HttpResponseNotFound("vendor with specified id not found!")
    transaction = ChargeTransaction()
    transaction.vendor = vendor
    transaction.charge(charge)

    return HttpResponse()
