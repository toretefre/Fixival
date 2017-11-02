from django import forms
from .models import Backline, Tekniske_behov, Bestilling, Band


class PostBehov(forms.ModelForm):

    class Meta:
        model = Tekniske_behov
        fields = ('band', 'backline', 'behov')


class PostBackline(forms.ModelForm):

    class Meta:
        model = Backline
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
