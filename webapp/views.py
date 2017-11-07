# -*- coding: utf-8 -

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Konserter, Band, Scener, Tekniske_behov, Backline, Bestilling
from django.shortcuts import render, redirect
from .forms import PostBehov, PostBackline, PostBestilling, PostBand
from django.utils import timezone
from datetime import datetime

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
        backline = Backline.objects.all()
        behov = Tekniske_behov.objects.all()
        return render(request, "webapp/tekniker_view.html", {'konserts': konserter, 'backline' : backline, 'behov' : behov})
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
        backline = Backline.objects.all()
        behov = Tekniske_behov.objects.all()
        today = timezone.now()

        for konsert in konserter:
            # Hent alle konserter som skal skjer nå eller i framtiden
            if konsert.dato >= today:
                # Hent alle band derfra fordi der ligger bare godkjente band
                        # Har gått gjennom bestillingen
                for band in konsert.band.all():
                    if band not in godkjente_bands:
                        godkjente_bands.append(band)

        return render(request, 'webapp/bookingansvarlig_tekniske_behov.html', {"bands":godkjente_bands, 'backline' : backline, 'behov' : behov})

    else:
        raise PermissionDenied

@login_required
def bookingansvarlig_bestilling_view(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        if request.method == "POST":
            form = PostBestilling(request.POST)
            form_band = PostBand(request.POST)
            if form.is_valid() and form_band.is_valid():
                if not Band.objects.filter(navn=request.POST['navn']).exists():
                    bestilling = form.save(commit=False)
                    band = form_band.save(commit=False)
                    band.kostnad = 0         #Default verdier
                    band.rating = 0          #Default verdier
                    band.manager = request.user
                    band.save()
                    bestilling.band = band
                    bestilling.godkjent = None
                    bestilling.save()
                else:
                    bestilling = form.save(commit=False)
                    band = Band.objects.get(navn=request.POST['navn'])
                    bestilling.band = band
                    bestilling.godkjent = None
                    bestilling.save()

                return render(request, 'webapp/bookingansvarlig_bestilling.html', {'form': form, 'form_band': form_band,'response':"Bestilling sendt"})
        else:
            form = PostBestilling()
            form_band = PostBand()
        return render(request, 'webapp/bookingansvarlig_bestilling.html', {'form': form, 'form_band': form_band})

@login_required
def manager_mainpage(request):
    if request.user.groups.filter(name='manager').exists():
        band = Band.objects.filter(manager = request.user)
        backline = Backline.objects.all()
        behov = Tekniske_behov.objects.all()
        backline_form = PostBackline()

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

login_required
def bookingsjef_prisgenerator(request):
    if request.user.groups.filter(name="bookingsjef").exists():
        konserts = Konserter.objects.all()
        if request.method == "POST":
            relevantKonsert=""
            if 'konsertliste' in request.POST:
                relevantKonsert = Konserter.objects.get(konsert=request.POST["konsertliste"])
                bandcost = 0
                bandpopularity = 0
                bandamount = 0
                # Iterer over alle band i konserten, finner gjennomsnittlig popularitet, antall band og samlet kostnad
                if relevantKonsert.band.all().count() == 0:
                    return render(request,'webapp/bookingsjef_prisgenerator.html',{"konserter":konserts,"error":"Konserten har ingen band. Book et band til denne konserten eller kontakt systemansvarlig om du tror det er feil."})
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
            if "Artist" in request.POST:
                selected_band = Band.objects.get(navn=request.POST['Artist'])
                return render(request, 'webapp/bookingansvarlig_artister.html', {'artist': selected_band, 'band': band})
            return render(request, 'webapp/bookingansvarlig_artister.html', {'band': band,"error":"Ingen band valgt"})
        return render(request, 'webapp/bookingansvarlig_artister.html', {'band': band})
    else:
        raise PermissionDenied

@login_required
def bookingsjef_bandtilbud(request):
    if request.user.groups.filter(name="bookingsjef").exists():
        tilbud = Bestilling.objects.filter(godkjent=None)
        if request.method == "POST":
            respons = ""
            months = {"januar":"01","februar":"02","mars":"03","april":"04","mai":"05","juni":"06","juli":"07","august":"08","september":"09","oktober":"10","november":"11","desember":"12"}
            if Band.objects.filter(navn=request.POST["tilbud"]).exists():
                valgt_band = Band.objects.get(navn=request.POST["tilbud"])
            else:
                return render(request, 'webapp/bookingsjef_bandtilbud.html',{"tilbud": tilbud})
            bestillingsdato = request.POST["dato"]
            datolist = bestillingsdato.split(" ")
            datolist[1] = months[datolist[1]]
            bestillingsdato = " ".join(datolist)
            valgt_bestilling = Bestilling.objects.get(band=valgt_band,dato=datetime.strptime(bestillingsdato,"%d. %m %Y %H:%M"),godkjent=None)
            if request.POST["answer"] == "True":
                respons = "Bestilling godkjent"
                valgt_bestilling.godkjent = True
                valgt_bestilling.save()
                valgt_band.kostnad = valgt_bestilling.pris
                valgt_band.save()
                if Konserter.objects.filter(dato=valgt_bestilling.dato).exists():
                    if not extraConf in request.POST:
                        return render(request, 'webapp/bookingsjef_bandtilbud.html',{"tilbud":tilbud,"chosenTilbud":valgt_bestilling})
                    if request.POST[extraConf] == "True":
                        konsert = Konserter.objects.get(dato=valgt_bestilling.dato)
                        konsert.band.add(valgt_band)
                        konsert.save()
                else:
                    konsert=Konserter.objects.create(
                    scene = valgt_bestilling.scene,
                    konsert = valgt_band.navn,
                    publikumsantall = 0,
                    festival="UKA")
                    konsert.save()
                    konsert.band.add(valgt_band)
                    konsert.save()
            else:
                respons = "Bestilling avslått"
                valgt_bestilling.godkjent = False
                valgt_bestilling.save()
            return render(request, 'webapp/bookingsjef_bandtilbud.html',{"tilbud":tilbud, "respons":respons})

        return render(request, 'webapp/bookingsjef_bandtilbud.html',{"tilbud": tilbud})

@login_required
def bookingansvarlig_tidligere_artister(request):
    if request.user.groups.filter(name="bookingansvarlig").exists():
        konserter = Konserter.objects.all()
        tidligere_konserter = []
        scene_tabell = []
        today = timezone.now()
        relevant_konsert = []
        for konsert in konserter:
            if konsert.dato < today:
                tidligere_konserter.append(konsert)

        if request.method == 'POST':
            all_bands = Band.objects.all()
            all_bandnames = []
            for band in all_bands:
                all_bandnames.append(band.navn)
            if request.POST['search_box'] in all_bandnames:
                band = Band.objects.get(navn= request.POST['search_box'])
                for konsert in tidligere_konserter:
                    for iterable_band in konsert.band.all():
                        if iterable_band == band:
                          relevant_konsert.append(str(konsert.scene))
                          relevant_konsert.append(konsert.dato.strftime("%d-%m-%Y %H:%M"))
                datostring = ", ".join(relevant_konsert)
                return render(request, 'webapp/bookingansvarlig_tidligere_artister.html', {'band': band, 'tidligere_konserter':tidligere_konserter, "datostring" : datostring})
            return render(request, 'webapp/bookingansvarlig_tidligere_artister.html', {'error': "Band har ikke spilt her"})
        return render(request, 'webapp/bookingansvarlig_tidligere_artister.html')

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

@login_required
def bookingsjef_oversikt(request):
    if request.user.groups.filter(name="bookingsjef").exists():
        today = timezone.now()
        relevante_bestillinger = Bestilling.objects.filter(dato__range=[today, today + timezone.timedelta(days=31)])
        godkjente_bestillinger = relevante_bestillinger.filter(godkjent = True)
        gb_datoer_stygt = []
        sendte_bestillinger = relevante_bestillinger.filter(godkjent = None)
        sb_datoer_stygt = []

        for bestilling in godkjente_bestillinger:
            gb_datoer_stygt.append(bestilling.dato)
        for bestilling in sendte_bestillinger:
            sb_datoer_stygt.append(bestilling.dato)

        alle_datoer_stygt = [today + timezone.timedelta(days=x) for x in range(31)]
        alle_datoer = [datetime.strftime(d, '%m-%d-%Y') for d in alle_datoer_stygt]
        gb_datoer = [datetime.strftime(d, '%m-%d-%Y') for d in gb_datoer_stygt]
        sb_datoer = [datetime.strftime(d, '%m-%d-%Y') for d in sb_datoer_stygt]
        ledige_datoer = list(set(alle_datoer) - set(gb_datoer))


        return render(request, 'webapp/bookingsjef_oversikt.html',{"godkjente_bestillinger": godkjente_bestillinger, "gb_datoer":gb_datoer, "sendte_bestillinger": sendte_bestillinger, "sb_datoer":sb_datoer, "ledige_datoer": ledige_datoer})
    else:
        raise PermissionDenied

@login_required
def pr_ansvarlig_mainpage(request):
    if request.user.groups.filter(name = "PR_ansvarlig").exists():
        return render(request, 'webapp/pr_ansvarlig.html')
    else:
        raise PermissionDenied

@login_required
def pr_ansvarlig_bookede_band(request):
    if request.user.groups.filter(name="PR_ansvarlig").exists():
        godkjente_bestillinger = Bestilling.objects.filter(godkjent = True)
        bookede_band = []
        for bestilling in godkjente_bestillinger:
            bookede_band.append(bestilling.band)

        return render(request, 'webapp/pr_ansvarlig_bookede_band.html', {"bookede_band": bookede_band})
    else:
        raise PermissionDenied
