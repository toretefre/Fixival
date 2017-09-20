from django.shortcuts import render
from .models import Konserter

# Create your views here.
def arrangoer_mainpage(request):
    konserts = Konserter.objects.all()
    return render(request,'webapp/arrangoer_mainpage.html',{'konserts':konserts})
