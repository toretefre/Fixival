from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Konserter, Band, Scener, Bestilling
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import PostBestilling, PostBand

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
    if len(request.user.groups.all()) > 0:
        return HttpResponseRedirect(reverse(str(request.user.groups.all()[0])))
    else:
        raise PermissionDenied

@login_required
def arrangoer(request):
    if request.user.groups.filter(name="arrangoer").exists():
        return render(request,'webapp/arrangoer.html',{})
    else:
        raise PermissionDenied


@login_required
def tech_view(request):
    if request.user.groups.filter(name="tekniker").exists():
        konserter = Konserter.objects.filter(teknikere = request.user)
        return render(request, "webapp/tekniker_view.html", {'konserts': konserter})
    else:
        raise PermissionDenied

@login_required
def bookingansvarlig(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        return render(request,'webapp/bookingansvarlig.html',{})
    else:
        raise PermissionDenied

@login_required
def bookingansvarlig_tidligere_konserter(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        konserter = Konserter.objects.all()
        sjangre = ["-----"]
        tidligere_konserter = []
        kommende_festivaler = []
        tidligere_festivaler = []
        today = timezone.now()
        for konsert in konserter:
            # Går gjennom alle band i en konsert
            for band in konsert.band.all():
                # Finner alle individuelle sjangre
                if band.sjanger not in sjangre:
                    sjangre.append(band.sjanger)
            # Finner alle konserter hvor dato er senere enn dagens
            if konsert.festival not in kommende_festivaler and konsert.dato > today:
                kommende_festivaler.append(konsert.festival)
            # Finner alle konserter hvor dato er tidligere enn dagens, kunne sikkert hatt "else"
            if konsert.festival not in tidligere_festivaler and konsert.dato <= today:
                tidligere_festivaler.append(konsert.festival)
        # Fjerner pågående festivaler, festivaler med konserter både vært og kommende.
        for festival in tidligere_festivaler:
            if festival in kommende_festivaler:
                tidligere_festivaler.remove(festival)
        # Finner konserter som har vært
        for konsert in konserter:
            if konsert.festival in tidligere_festivaler:
                tidligere_konserter.append(konsert)

        return render(request,'webapp/bookingansvarlig_tidligere_konserter.html',{"tidligere_konserter":tidligere_konserter,"sjangre":sjangre})
    else:
        raise PermissionDenied

@login_required
def bookingansvarlig_tekniske_behov(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        godkjente_bands = []
        konserter = Konserter.objects.all()
        today = timezone.now()

        for konsert in konserter:
            # Hent alle konserter som skal skjer nå eller i framtiden
            if konsert.dato >= today:
                # Hent alle band derfra fordi der ligger bare godkjente band
                        # Har gått gjennom bestillingen
                for band in konsert.band.all():
                    godkjente_bands.append(band)

        return render(request, 'webapp/bookingansvarlig_tekniske_behov.html', {"bands":godkjente_bands})
    else:
        raise PermissionDenied

@login_required
def bookingansvarlig_bestilling_view(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        if request.method == "POST":
            form = PostBestilling(request.POST)
            form_band = PostBand(request.POST)
            if form.is_valid() and form_band.is_valid():
                bestilling = form.save(commit=False)
                band = form_band.save(commit=False)
                band.kostnad = 0         #Default verdier
                band.rating = 0          #Default verdier
                band.manager = request.user
                band.save()
                bestilling.band = band
                bestilling.godkjent = None
                bestilling.save()

                return render(request, 'webapp/bookingansvarlig.html', {'form': form, 'form_band': form_band,'response':"Bestilling sendt"})
        else:
            form = PostBestilling()
            form_band = PostBand()
        return render(request, 'webapp/bookingansvarlig.html', {'form': form, 'form_band': form_band})

def bookingsjef_prisgenerator(request):
    if request.user.groups.filter(name="bookingsjef").exists():
        konserts = Konserter.objects.all()
        if request.method == "POST":
            if 'konsertliste' in request.POST:
                relevantKonsert = Konserter.objects.get(konsert=request.POST["konsertliste"])
                bandcost = 0
                bandpopularity = 0
                bandamount = 0
                # Iterer over alle band i konserten, finner gjennomsnittlig popularitet, antall band og samlet kostnad
                for band in relevantKonsert.band.all():
                    bandcost += band.kostnad
                    bandpopularity += band.rating
                    bandamount += 1
                # Regner gjennomsnittet nevnt over
                bandpopularity = int(bandpopularity / bandamount)

                scenecosts = {}
                allScener = Scener.objects.all()
                # Bruker den sykt kreative, sykt avanserte formelen for å regne ut prisforslag per billett.
                # Dette legges i en dict med key scenenavn og item prisforslag
                for scene in allScener:
                    scenecosts[scene] = int((scene.kostnad + bandcost) / scene.storrelse + 5*bandpopularity)
            else:
                scenecosts = {"Konsert": "ikke funnet"}
            return render(request,'webapp/bookingsjef_prisgenerator.html',{"konserter":konserts,"scenecost":scenecosts,"valgtkonsert":relevantKonsert})
        else:
            return render(request,'webapp/bookingsjef_prisgenerator.html',{"konserter":konserts})

@login_required
def bookingansvarlig_artister(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        band = Band.objects.all()
        if request.method == "POST":
            selected_band = Band.objects.get(navn=request.POST['Artist'])
            return render(request, 'webapp/bookingansvarlig_artister.html', {'artist': selected_band, 'band': band})

        return render(request, 'webapp/bookingansvarlig_artister.html', {'band': band})
    else:
        raise PermissionDenied

@login_required
def bookingsjef_rapport(request):
    if request.user.groups.filter(name="bookingsjef").exists():
        scener = Scener.objects.all()
        if request.method == "POST":
            if 'scenerapport' in request.POST:
                scene = Scener.objects.get(navn=request.POST['scenerapport'])
                konserter = Konserter.objects.filter(scene=scene)
                konsertinfo = {}
                for konsert in konserter:
                    kostnad = konsert.scene.kostnad
                    for band in konsert.band.all():
                        kostnad += band.kostnad
                    resultat = konsert.billettpris * konsert.publikumsantall - kostnad
                    konsertinfo[konsert] = {"kostnad":kostnad,"publikumsantall":konsert.publikumsantall,"resultat":resultat}
                return render(request,'webapp/bookingsjef_rapport.html',{"konsertinfo":konsertinfo,"scener":scener,"valgtscene":scene})
        return render(request, 'webapp/bookingsjef_rapport.html',{"scener":scener})
    else:
        raise PermissionDenied
