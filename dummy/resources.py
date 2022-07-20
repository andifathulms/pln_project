import imp
from pyexpat import model
from import_export import resources
from .models import DummyTable

class DummyTableResource(resources.ModelResource):
    class meta:
        model = DummyTable
        exclude = ('id',)