from django.db import models

from document.models import PRK
from account.models import Account

class UsulanRekomposisi(models.Model):
    proposed_by     = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    prk             = models.ForeignKey(PRK, on_delete=models.CASCADE, blank=True, null=True)
    upload_date     = models.DateTimeField(blank=True, null=True)
    last_edit_date  = models.DateTimeField(blank=True, null=True)
    jan             = models.IntegerField()
    feb             = models.IntegerField()
    mar             = models.IntegerField()
    apr             = models.IntegerField()
    mei             = models.IntegerField()
    jun             = models.IntegerField()
    jul             = models.IntegerField()
    aug             = models.IntegerField()
    sep             = models.IntegerField()
    okt             = models.IntegerField()
    nov             = models.IntegerField()
    des             = models.IntegerField()
    notes           = models.TextField()
