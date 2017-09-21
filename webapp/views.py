from django.shortcuts import render
from .models import Konserter
# Create your views here.
def tech_view(request):
    konserter = Konserter.objects.all()
    users = User.objects.all()
    return render(request, "webapp/tekniker_view.html", {'konserts':konserter}, {'brukere':users})
