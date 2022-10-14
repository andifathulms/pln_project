from email.policy import default
from django.db import models
from datetime import datetime

# from document.models import PRK
from account.models import Account

class UsulanPeriod(models.Model):
    start_date      = models.DateField()
    end_date        = models.DateField()
    for_rekom_aki   = models.BooleanField(default=False)
    for_rekom_akb   = models.BooleanField(default=False)
    created_by      = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    status          = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.start_date.strftime("%m/%d/%Y") + " - " + self.end_date.strftime("%m/%d/%Y")

    def is_in_period(self):
        return datetime.date(datetime.now()) >= self.start_date and datetime.date(datetime.now()) <= self.end_date
    
    def is_before_period(self):
        return datetime.date(datetime.now()) < self.start_date
    
    def start_date_str(self):
        return self.start_date.strftime("%m/%d/%Y")
    
    def end_date_str(self):
        return self.end_date.strftime("%m/%d/%Y")

class UsulanRekomposisi(models.Model):
    period          = models.ForeignKey(UsulanPeriod, on_delete=models.CASCADE, blank=True, null=True)
    proposed_by     = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    upload_date     = models.DateTimeField(blank=True, null=True)
    last_edit_date  = models.DateTimeField(blank=True, null=True)
    division        = models.CharField(max_length=10,blank=True, null=True)
    is_draft        = models.BooleanField(default=True)
    is_publish      = models.BooleanField(default=False)
    revisi          = models.CharField(max_length=3, default="AKI")

    is_data_created = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Rekom " + self.revisi + " " + self.period.__str__() + " - " + self.division

class UsulanRekomposisiData(models.Model):
    file            = models.ForeignKey('UsulanRekomposisi', on_delete=models.CASCADE)
    prk             = models.ForeignKey('document.PRK', on_delete=models.CASCADE, blank=True, null=True)
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
    is_changed      = models.BooleanField(default=False)
    edited_by       = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.is_changed) + " - " +  self.prk.rekap_user_induk + " - " + self.prk.no_prk + " Rekom " + self.file.revisi

    def get_rencana_bulan(self, month):
        switch = {
            1: int(self.jan or 0),2: int(self.feb or 0),3: int(self.mar or 0),
            4: int(self.apr or 0),5: int(self.mei or 0),6: int(self.jun or 0),
            7: int(self.jul or 0),8: int(self.aug or 0),9: int(self.sep or 0),
            10: int(self.okt or 0),11: int(self.nov or 0),12: int(self.des or 0)
        }

        return switch[month]
    
    def is_missing_notes(self):
        bool_month = bool(self.jan or self.feb or self.mar or self.apr or self.mei or self.jun or self.jul or self.aug or self.sep or self.okt or self.nov or self.des)
        bool_notes = bool(self.notes)
        return bool_notes == False and bool_month == True
    
    def is_rencana_bulan(self, month):
        switch = {
            1: self.jan,2: self.feb,3: self.mar,
            4: self.apr,5: self.mei,6: self.jun,
            7: self.jul,8: self.aug,9: self.sep,
            10: self.okt,11: self.nov,12: self.des
        }

        return switch[month] != None
    
    def get_total_edit(self):
        return sum([int(self.get_rencana_bulan(i) or 0) for i in range(1,13)])
    
    def sum_usulan(self):
        return int(self.jan or 0) + int(self.feb or 0) + int(self.mar or 0) + int(self.apr or 0) + int(self.mei or 0) + int(self.jun or 0) + int(self.jul or 0) + int(self.aug or 0) + int(self.sep or 0) + int(self.okt or 0) + int(self.nov or 0) + int(self.des or 0)
    
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

class EbudgetFile(models.Model):

    file = models.FileField(upload_to='monev/ebudget')

class EbudgetFileOutput(models.Model):

    file = models.FileField(upload_to='monev/ebudget/output')