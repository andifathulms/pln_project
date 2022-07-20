from unicodedata import name
from django.db import models

class DummyTable(models.Model):
    name        = models.CharField(max_length=100)
    field1      = models.CharField(max_length=100)
    field2      = models.TextField()
    field3      = models.IntegerField()
    field4      = models.CharField(max_length=100)
