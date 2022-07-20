from dataclasses import field
from pyexpat import model
from django import forms

from .models import DummyFileUpload

class DummyFileUploadForm(forms.ModelForm):

    class Meta:
        model = DummyFileUpload
        fields = ('period', 'year', 'status', 'notes')