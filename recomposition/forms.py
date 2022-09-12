from django import forms

from .models import UsulanPeriod

class UsulanPeriodForm(forms.ModelForm):

    class Meta:
        model = UsulanPeriod
        fields = '__all__'
        exclude = ('created_by','status' )
