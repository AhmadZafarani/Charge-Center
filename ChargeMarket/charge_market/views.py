from django.http import HttpRequest, HttpResponse


def add_vendor(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world!")
