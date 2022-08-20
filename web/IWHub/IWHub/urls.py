"""IWHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from presets.views import logout_view, signin_view, signup_view

def test(request):
    msg = "Test"
    return HttpResponse(f"{msg}\n\n{request}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('presets.urls')),
    path('signin/', signin_view, name="sign_in"),
    path('signup/', signup_view, name="sign_up"),
    path('logout/', logout_view, name="logout"),

    re_path(r'.*', test)
]