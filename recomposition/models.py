from django.db import models

from document.models import PRK
from account.models import Account

class UsulanPeriod(models.Model):
    start_date      = models.DateField()
    end_date        = models.DateField()

class UsulanRekomposisi(models.Model):
    proposed_by     = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    upload_date     = models.DateTimeField(blank=True, null=True)
    last_edit_date  = models.DateTimeField(blank=True, null=True)
    for_month       = models.PositiveIntegerField()
    division        = models.CharField(max_length=10,blank=True, null=True)
    is_draft        = models.BooleanField(default=True)
    is_publish      = models.BooleanField(default=False)

class UsulanRekomposisiData(models.Model):
    file            = models.ForeignKey('UsulanRekomposisi', on_delete=models.CASCADE)
    prk             = models.ForeignKey(PRK, on_delete=models.CASCADE, blank=True, null=True)
    jan             = models.IntegerField(blank=True, null=True)
    feb             = models.IntegerField(blank=True, null=True)
    mar             = models.IntegerField(blank=True, null=True)
    apr             = models.IntegerField(blank=True, null=True)
    mei             = models.IntegerField(blank=True, null=True)
    jun             = models.IntegerField(blank=True, null=True)
    jul             = models.IntegerField(blank=True, null=True)
    aug             = models.IntegerField(blank=True, null=True)
    sep             = models.IntegerField(blank=True, null=True)
    okt             = models.IntegerField(blank=True, null=True)
    nov             = models.IntegerField(blank=True, null=True)
    des             = models.IntegerField(blank=True, null=True)
    notes           = models.TextField(blank=True, null=True)

    def insertToMonth(self, month, value):
        
        if month == 1:
            self.jan = value
            self.save()
        elif month == 2:
            self.feb = value
            self.save()
        elif month == 3:
            self.mar = value
            self.save()
        elif month == 4:
            self.apr = value
            self.save()
        elif month == 5:
            self.mei = value
            self.save()
        elif month == 6:
            self.jun = value
            self.save()
        elif month == 7:
            self.jul = value
            self.save()
        elif month == 8:
            self.aug = value
            self.save()
        elif month == 9:
            self.sep = value
            self.save()
        elif month == 10:
            self.okt = value
            self.save()
        elif month == 11:
            self.nov = value
            self.save()
        elif month == 12:
            self.des = value
            self.save()
