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
        return int(self.ai_this_year)

    def real_aki(self):
        return int(self.aki_this_year)

class Assigned_PRK(models.Model):
    file               = models.FileField(upload_to='monev/prk_code')

class PRK_Lookup(models.Model):
    file                    = models.ForeignKey('Assigned_PRK', on_delete=models.CASCADE, blank=True, null=True)
    no_prk                  = models.CharField(max_length=100, blank=True, null=True)
    kode_prk                = models.CharField(max_length=100, blank=True, null=True)
    kode_bpo                = models.CharField(max_length=100, blank=True, null=True)
    rekap_user_induk        = models.CharField(max_length=100, blank=True, null=True)
