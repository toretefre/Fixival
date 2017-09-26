from django.shortcuts import render
from .models import Konserter

# Create your views here.
def arrangoer_mainpage(request):
    konserts = Konserter.objects.all()
    return render(request,'webapp/arrangoer_mainpage.html',{'konserts':konserts})

def oversiktsview_konserter(request):
    konserter = Konserter.objects.all()
    scener = []
    for konsert in konserter:
        if konsert.scene not in scener:
            scener.append(konsert.scene)

    return render(request, 'webapp/oversiktsview_konserter.html', {'konserter':konserter, 'scener':scener})
