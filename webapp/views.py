from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

def login():
    return HttpResponse("login")


@login_required
def logout(request):
    return HttpResponse("User logged out")
