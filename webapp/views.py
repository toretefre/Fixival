
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Konserter
from django.shortcuts import render
# Create your views here.
@login_required
def arrangoer_mainpage(request):
    if request.user.groups.filter(name="arrangoer").exists():
        konserts = Konserter.objects.all()
        return render(request,'webapp/arrangoer_mainpage.html',{'konserts':konserts})
    else:
        raise PermissionDenied

@login_required
def oversiktsview_konserter(request):
    if request.user.groups.filter(name="arrangoer").exists():
        konserter = Konserter.objects.all()
        scener = []
        for konsert in konserter:
            if konsert.scene not in scener:
                scener.append(konsert.scene)
        return render(request, 'webapp/oversiktsview_konserter.html', {'konserter':konserter, 'scener':scener})
    else:
        raise PermissionDenied

def login():
    return HttpResponse("login")


@login_required
def logout(request):
    return HttpResponse("User logged out")

@login_required
def redirect_login(request):
    return HttpResponseRedirect(reverse(str(request.user.groups.all()[0])))

@login_required
def arrangoer(request):
    return render(request,'webapp/arrangoer.html',{})


@login_required
def tech_view(request):
    if request.user.groups.filter(name="teknikker").exists():
        konserter = Konserter.objects.filter(teknikere__icontains = request.user)
        users = User.objects.all()
        return render(request, "webapp/tekniker_view.html", {'konserts': konserter}, {'brukere': users})
    else:
        raise PermissionDenied

