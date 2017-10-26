from django import forms
<<<<<<< HEAD
from .models import Backline, Tekniske_behov

class PostBehov(forms.ModelForm):

    class Meta:
        model = Tekniske_behov
        fields = ('band', 'backline', 'behov')

class PostBackline(forms.ModelForm):

    class Meta:
        model = Backline
        fields = ('band', 'backline')
=======

from .models import Bestilling, Band



class PostBestilling(forms.ModelForm):

    class Meta:
        model = Bestilling
        fields = ('dato', 'scene', 'pris')

class PostBand(forms.ModelForm):
    navn = forms.CharField(label="Band")

    class Meta:
        model = Band
        fields = {'navn'}
>>>>>>> master
