from django import forms
from .models import AnimalReport

class AnimalReportForm(forms.ModelForm):
    class Meta:
        model = AnimalReport
        fields = '__all__'
