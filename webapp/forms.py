from django import forms
from .models import Backline, Tekniske_behov

class PostBehov(forms.ModelForm):

    class Meta:
        model = Tekniske_behov
        fields = ('band', 'backline', 'behov')

class PostBackline(forms.ModelForm):

    class Meta:
        model = Backline
        fields = ('band', 'backline')
