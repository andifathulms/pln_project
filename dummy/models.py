from django.db import models
from django.utils import timezone
from account.models import Account

class DummyTable(models.Model):
    dummy_file  = models.ForeignKey('DummyFileUpload', on_delete=models.CASCADE, related_name='file_parent')

    #Example field
    name        = models.CharField(max_length=100)
    field1      = models.CharField(max_length=100)
    field2      = models.TextField()
    field3      = models.IntegerField()
    field4      = models.CharField(max_length=100)

class DummyFileUpload(models.Model):
    uploader    = models.ForeignKey(Account, on_delete=models.CASCADE)
    filename    = models.CharField(max_length=200)
    period      = models.CharField(max_length=100)
    year        = models.IntegerField()
    status      = models.CharField(max_length=100)
    notes       = models.CharField(max_length=200, blank=True, null=True)
    date_uploaded   = models.DateTimeField(default=timezone.now)
    submission      = models.CharField(max_length=100, default="Telah Disetujui")

    def __str__(self):
        return str(self.year) + " - " + self.status
