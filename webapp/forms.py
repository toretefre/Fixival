from django import forms
from .models import Backline, Tekniske_behov, Bestilling, Band

#lager formet for å kunne poste tekniske behov
class PostBehov(forms.ModelForm):

    class Meta:
        #velger hvilken model som brukes i formen
        model = Tekniske_behov
        #velger hvilke felter fra elementet som skal brukes i formet
        fields = ('band', 'backline', 'behov')

#lager formet for å kunne poste backline
class PostBackline(forms.ModelForm):

    class Meta:
        #velger hvilken model som brukes i formen
        model = Backline
        #velger hvilke felter fra elementet som skal brukes i formet
        fields = ('band', 'backline')


class PostBestilling(forms.ModelForm):

    class Meta:
        model = Bestilling
        fields = ('dato', 'scene', 'pris')
        help_texts = {
            'dato': '<br>Eksempelinput: 1999-12-31 23:59',
        }


class PostBand(forms.ModelForm):
    navn = forms.CharField(label="Band")

    class Meta:
        model = Band
        fields = {'navn'}
