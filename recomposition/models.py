from django.db import models

from document.models import PRK
from account.models import Account

class UsulanPeriod(models.Model):
    start_date      = models.DateField()
    end_date        = models.DateField()

class UsulanRekomposisi(models.Model):
    period          = models.ForeignKey(UsulanPeriod, on_delete=models.CASCADE, blank=True, null=True)
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

    def get_rencana_bulan(self, month):
        switch = {
            1: int(self.jan or 0),2: int(self.feb or 0),3: int(self.mar or 0),
            4: int(self.apr or 0),5: int(self.mei or 0),6: int(self.jun or 0),
            7: int(self.jul or 0),8: int(self.aug or 0 or 0),9: int(self.sep or 0),
            10: int(self.okt or 0),11: int(self.nov or 0),12: int(self.des or 0)
        }

        return switch[month]
    
    def insertToMonth(self, monthS, value):
        month = int(monthS)
        if month == 1:
            try:
                self.jan = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 2:
            try:
                self.feb = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 3:
            try:
                self.mar = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 4:
            try:
                self.apr = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 5:
            try:
                self.mei = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 6:
            try:
                self.jun = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 7:
            try:
                self.jul = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 8:
            try:
                self.aug = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 9:
            try:
                self.sep = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 10:
            try:
                self.okt = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 11:
            try:
                self.nov = value
                self.save()
            except Exception as e:
                print(e)
        elif month == 12:
            try:
                self.des = value
                self.save()
            except Exception as e:
                print(e)
        else:
            print(month)
