from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

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
