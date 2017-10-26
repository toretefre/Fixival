from django import forms

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