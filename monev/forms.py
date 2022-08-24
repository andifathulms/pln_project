from django import forms

from .models import LRPA_File, FileMouPengalihan

class LRPAFileForm(forms.ModelForm):

    class Meta:
        model = LRPA_File
        fields = '__all__'
        exclude = ('upload_by', )

class MouFileForm(forms.ModelForm):

    class Meta:
        model = FileMouPengalihan
        fields = '__all__'
        exclude = ('upload_by', )