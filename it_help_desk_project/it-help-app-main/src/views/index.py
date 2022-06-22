from django.http import HttpResponse

def as_view(request) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the IT Help landing page")
