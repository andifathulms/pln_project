from django.db import models
from datetime import date
from account.models import Account

class LRPA_File(models.Model):
    lrpa_file               = models.FileField(upload_to='monev/lrpa')
    upload_date             = models.DateTimeField(auto_now_add=True)
    upload_by               = models.ForeignKey(Account, on_delete=models.CASCADE)
    file_export_date        = models.DateField(default=date.today)
    for_month               = models.IntegerField()
    for_year                = models.IntegerField()

class LRPA_Monitoring(models.Model):
    file                    = models.ForeignKey('LRPA_File', on_delete=models.CASCADE, blank=True, null=True)
    no_prk                  = models.CharField(max_length=100, blank=True, null=True)
    disburse_year_before    = models.CharField(max_length=100, blank=True, null=True)
    mekanisme_pembayaran    = models.CharField(max_length=100, blank=True, null=True)
    jan_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    jan_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    feb_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    feb_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    mar_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    mar_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    apr_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    apr_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    mei_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    mei_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    jun_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    jun_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    jul_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    jul_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    aug_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    aug_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    sep_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    sep_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    okt_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    okt_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    nov_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    nov_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    des_rencana_disburse    = models.CharField(max_length=100, blank=True, null=True)
    des_realisasi_disburse  = models.CharField(max_length=100, blank=True, null=True)
    ai_this_year            = models.FloatField(blank=True, null=True)
    aki_this_year           = models.FloatField(blank=True, null=True)

    def real_ai(self):
        return int(self.ai_this_year or 0)

    def real_aki(self):
        return int(self.aki_this_year or 0)
    
    def sum_realisasi(self):
        return int(self.jan_realisasi_disburse) + int(self.feb_realisasi_disburse) + int(self.mar_realisasi_disburse) + int(self.apr_realisasi_disburse) + int(self.mei_realisasi_disburse) + int(self.jun_realisasi_disburse) + int(self.jul_realisasi_disburse) + int(self.aug_realisasi_disburse) + int(self.sep_realisasi_disburse) + int(self.okt_realisasi_disburse) + int(self.nov_realisasi_disburse) + int(self.des_realisasi_disburse)

    def get_rencana_bulan(self, month):
        switch = {
            1: int(self.jan_rencana_disburse),2: int(self.feb_rencana_disburse),3: int(self.mar_rencana_disburse),
            4: int(self.apr_rencana_disburse),5: int(self.mei_rencana_disburse),6: int(self.jun_rencana_disburse),
            7: int(self.jul_rencana_disburse),8: int(self.aug_rencana_disburse or 0),9: int(self.sep_rencana_disburse),
            10: int(self.okt_rencana_disburse),11: int(self.nov_rencana_disburse),12: int(self.des_rencana_disburse)
        }

        return switch[month]
    
    def get_realisasi_bulan(self, month):
        switch = {
            1: int(self.jan_realisasi_disburse),2: int(self.feb_realisasi_disburse),3: int(self.mar_realisasi_disburse),
            4: int(self.apr_realisasi_disburse),5: int(self.mei_realisasi_disburse),6: int(self.jun_realisasi_disburse),
            7: int(self.jul_realisasi_disburse),8: int(self.aug_realisasi_disburse or 0),9: int(self.sep_realisasi_disburse),
            10: int(self.okt_realisasi_disburse),11: int(self.nov_realisasi_disburse),12: int(self.des_realisasi_disburse)
        }

        return switch[month]

class Assigned_PRK(models.Model):
    file               = models.FileField(upload_to='monev/prk_code')

class PRK_Lookup(models.Model):
    file                    = models.ForeignKey('Assigned_PRK', on_delete=models.CASCADE, blank=True, null=True)
    no_prk                  = models.CharField(max_length=100, blank=True, null=True)
    kode_prk                = models.CharField(max_length=100, blank=True, null=True)
    kode_bpo                = models.CharField(max_length=100, blank=True, null=True)
    rekap_user_induk        = models.CharField(max_length=100, blank=True, null=True)
    upp                     = models.CharField(max_length=100, blank=True, null=True)

class FileMouPengalihan(models.Model):
    mou_file                = models.FileField(upload_to='monev/mou_pengalihan')
    upload_date             = models.DateTimeField(auto_now_add=True)
    upload_by               = models.ForeignKey(Account, on_delete=models.CASCADE)
    file_export_date        = models.DateField(default=date.today)
    for_month               = models.IntegerField()
    for_year                = models.IntegerField()

class MouPengalihanData(models.Model):
    file                    = models.ForeignKey('FileMouPengalihan', on_delete=models.CASCADE, blank=True, null=True)
    no_prk                  = models.CharField(max_length=100, blank=True, null=True)
    mou                     = models.CharField(max_length=255, blank=True, null=True)
    ai_this_year            = models.FloatField(blank=True, null=True)
    aki_this_year           = models.FloatField(blank=True, null=True)
    jan                     = models.CharField(max_length=100, blank=True, null=True)
    feb                     = models.CharField(max_length=100, blank=True, null=True)
    mar                     = models.CharField(max_length=100, blank=True, null=True)
    apr                     = models.CharField(max_length=100, blank=True, null=True)
    mei                     = models.CharField(max_length=100, blank=True, null=True)
    jun                     = models.CharField(max_length=100, blank=True, null=True)
    jul                     = models.CharField(max_length=100, blank=True, null=True)
    aug                     = models.CharField(max_length=100, blank=True, null=True)
    sep                     = models.CharField(max_length=100, blank=True, null=True)
    okt                     = models.CharField(max_length=100, blank=True, null=True)
    nov                     = models.CharField(max_length=100, blank=True, null=True)
    des                     = models.CharField(max_length=100, blank=True, null=True)

    def get_realisasi_bulan(self, month):
        switch = {
            1: int(float(self.jan or 0)),2: int(float(self.feb or 0)),3: int(float(self.mar or 0)),
            4: int(float(self.apr or 0)),5: int(float(self.mei or 0)),6: int(float(self.jun or 0)),
            7: int(float(self.jul or 0)),8: int(float(self.aug or 0)),9: int(float(self.sep or 0)),
            10: int(float(self.okt or 0)),11: int(float(self.nov or 0)),12: int(float(self.des or 0))
        }

        return switch[month]
    
