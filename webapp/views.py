from django.shortcuts import render
from .models import Konserter

def oversiktsview_konserter(request):
    konserter = Konserter.objects.all()
    scener = []
    for konsert in konserter:
        if konsert.scene not in scener:
            scener.append(konsert.scene)

    return render(request, 'webapp/oversiktsview_konserter.html', {'konserter':konserter, 'scener':scener})
