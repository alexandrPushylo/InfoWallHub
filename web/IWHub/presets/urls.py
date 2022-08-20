from django.urls import path
from django.http import HttpResponse


def test(request):
    msg = "Test"
    return HttpResponse(f"{msg}\n\n{request}")


urlpatterns = [
    path('', test),


]