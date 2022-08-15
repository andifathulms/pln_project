from django import forms

from .models import LRPA_File

class LRPAFileForm(forms.ModelForm):

    class Meta:
        model = LRPA_File
        fields = '__all__'
        exclude = ('upload_by', )