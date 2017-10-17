from django.shortcuts import render
from .models import Tekniske_behov, Backline, Band
from django.http import HttpResponseRedirect
from .forms import PostBehov, PostBackline
from django.shortcuts import redirect


# Create your views here.
@login_required
def manager_mainpage(request):
    if request.user.groups.filter(name='manager').exists():
        band = Band.objects.all()
        backline = Backline.objects.all()
        behov = Tekniske_behov.objects.all()

        if request.method == 'POST' and 'submitBehov' in request.POST:
            behov_form = PostBehov(request.POST)
            if behov_form.is_valid():
                behov = behov_form.save(commit=False)
                behov.save()
                return redirect('webapp/manager_mainpage.html', pk=behov.pk)
        else:
            behov_form = PostBehov()

        if request.method == 'POST' and 'submitBackline' in request.POST:
            backline_form = PostBackline(request.POST)
            if backline_form.is_valid():
                backline = backline_form.save(commit=False)
                backline.save()
                return redirect('webapp/manager_mainpage.html', pk=backline.pk)
        else:
            backline_form = PostBackline()

        return render(request, 'webapp/manager_mainpage.html', {'band' : band, 'backline' : backline, 'behov' : behov, 'behov_form' : behov_form, 'backline_form' : backline_form})
    else:
        raise PermissionDenied
