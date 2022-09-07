from django.db import models
from account.models import Account

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from notification.models import Notification
from monev.models import LRPA_File, FileMouPengalihan
from recomposition.models import UsulanRekomposisiData

from datetime import datetime

def this_month():
    return datetime.now().month

class PRK(models.Model):
    no_prk              = models.CharField(max_length=255, unique=True)
    no_program          = models.PositiveIntegerField(blank=True, null=True)
    no_ruptl            = models.CharField(max_length=255, blank=True, null=True)
    cluster             = models.CharField(max_length=255, blank=True, null=True)
    fungsi              = models.CharField(max_length=255, blank=True, null=True)
    sub_fungsi          = models.CharField(max_length=255, blank=True, null=True)
    program_utama       = models.CharField(max_length=255, blank=True, null=True)
    score               = models.CharField(max_length=255, blank=True, null=True)
    jenis_program       = models.CharField(max_length=255, blank=True, null=True)
    keg_no              = models.PositiveIntegerField(blank=True, null=True)
    keg_uraian          = models.TextField(blank=True, null=True)
    kode_prk            = models.CharField(max_length=100, blank=True, null=True)
    kode_bpo            = models.CharField(max_length=100, blank=True, null=True)
    rekap_user_induk    = models.CharField(max_length=100, blank=True, null=True)
    upp                 = models.CharField(max_length=100, blank=True, null=True)

class PRKData(models.Model):
    file_lrpa               = models.ForeignKey(LRPA_File, on_delete=models.CASCADE, blank=True, null=True)
    file_mou                = models.ForeignKey(FileMouPengalihan, on_delete=models.CASCADE, blank=True, null=True)

    prk                     = models.ForeignKey('PRK', on_delete=models.CASCADE)
    prk_data_year           = models.PositiveIntegerField(default=2022)

    #FROM LRPA
    disburse_year_before    = models.CharField(max_length=100, blank=True, null=True)
    mekanisme_pembayaran    = models.CharField(max_length=100, blank=True, null=True)
    jan_rencana             = models.CharField(max_length=100, blank=True, null=True)
    jan_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    feb_rencana             = models.CharField(max_length=100, blank=True, null=True)
    feb_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    mar_rencana             = models.CharField(max_length=100, blank=True, null=True)
    mar_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    apr_rencana             = models.CharField(max_length=100, blank=True, null=True)
    apr_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    mei_rencana             = models.CharField(max_length=100, blank=True, null=True)
    mei_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    jun_rencana             = models.CharField(max_length=100, blank=True, null=True)
    jun_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    jul_rencana             = models.CharField(max_length=100, blank=True, null=True)
    jul_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    aug_rencana             = models.CharField(max_length=100, blank=True, null=True)
    aug_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    sep_rencana             = models.CharField(max_length=100, blank=True, null=True)
    sep_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    okt_rencana             = models.CharField(max_length=100, blank=True, null=True)
    okt_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    nov_rencana             = models.CharField(max_length=100, blank=True, null=True)
    nov_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    des_rencana             = models.CharField(max_length=100, blank=True, null=True)
    des_realisasi           = models.CharField(max_length=100, blank=True, null=True)
    ai_this_year            = models.FloatField(blank=True, null=True)
    aki_this_year           = models.FloatField(blank=True, null=True)

    #FROM MOU PENGALIHAN
    mou                     = models.CharField(max_length=255, blank=True, null=True)
    jan_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    feb_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    mar_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    apr_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    mei_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    jun_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    jul_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    aug_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    sep_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    okt_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    nov_pengalihan          = models.CharField(max_length=100, blank=True, null=True)
    des_pengalihan          = models.CharField(max_length=100, blank=True, null=True)

    def real_ai(self):
        return int(self.ai_this_year or 0)

    def real_aki(self):
        return int(self.aki_this_year or 0)
    
    def get_realisasi_month(self, m):
        month = this_month()
        if m == 1:
            if self.jan_pengalihan and month == m:
                return self.jan_pengalihan
            else:
                return self.jan_realisasi
        elif m == 2:
            if self.feb_pengalihan and month == m:
                return self.feb_pengalihan
            else:
                return self.feb_realisasi
        elif m == 3:
            if self.mar_pengalihan and month == m:
                return self.mar_pengalihan
            else:
                return self.mar_realisasi
        elif m == 4:
            if self.apr_pengalihan and month == m:
                return self.apr_pengalihan
            else:
                return self.apr_realisasi
        elif m == 5:
            if self.mei_pengalihan and month == m:
                return self.mei_pengalihan
            else:
                return self.mei_realisasi
        elif m == 6:
            if self.jun_pengalihan and month == m:
                return self.jun_pengalihan
            else:
                return self.jun_realisasi
        elif m == 7:
            if self.jul_pengalihan and month == m:
                return self.jul_pengalihan
            else:
                return self.jul_realisasi
        elif m == 8:
            if self.aug_pengalihan and month == m:
                return self.aug_pengalihan
            else:
                return self.aug_realisasi
        elif m == 9:
            if self.sep_pengalihan and month == m:
                return self.sep_pengalihan
            else:
                return self.sep_realisasi
        elif m == 10:
            if self.okt_pengalihan and month == m:
                return self.okt_pengalihan
            else:
                return self.okt_realisasi
        elif m == 11:
            if self.nov_pengalihan and month == m:
                return self.nov_pengalihan
            else:
                return self.nov_realisasi
        elif m == 12:
            if self.des_pengalihan and month == m:
                return self.des_pengalihan
            else:
                return self.des_realisasi
    
    def get_rencana_month(self, m):
        month = this_month()
        if m == 1:
            if m <= month:
                return self.jan_rencana
            elif m > month and self.jan_pengalihan:
                return self.jan_pengalihan
            else:
                return self.jan_rencana
        elif m == 2:
            if m <= month:
                return self.feb_rencana
            elif m > month and self.feb_pengalihan:
                return self.feb_pengalihan
            else:
                return self.feb_rencana
        elif m == 3:
            if m <= month:
                return self.mar_rencana
            elif m > month and self.mar_pengalihan:
                return self.mar_pengalihan
            else:
                return self.mar_rencana
        elif m == 4:
            if m <= month:
                return self.apr_rencana
            elif m > month and self.apr_pengalihan:
                return self.apr_pengalihan
            else:
                return self.apr_rencana
        elif m == 5:
            if m <= month:
                return self.mei_rencana
            elif m > month and self.mei_pengalihan:
                return self.mei_pengalihan
            else:
                return self.mei_rencana
        elif m == 6:
            if m <= month:
                return self.jun_rencana
            elif m > month and self.jun_pengalihan:
                return self.jun_pengalihan
            else:
                return self.jun_rencana
        elif m == 7:
            if m <= month:
                return self.jul_rencana
            elif m > month and self.jul_pengalihan:
                return self.jul_pengalihan
            else:
                return self.jul_rencana
        elif m == 8:
            if m <= month:
                return self.aug_rencana
            elif m > month and self.aug_pengalihan:
                return self.aug_pengalihan
            else:
                return self.aug_rencana
        elif m == 9:
            if m <= month:
                return self.sep_rencana
            elif m > month and self.sep_pengalihan:
                return self.sep_pengalihan
            else:
                return self.sep_rencana
        elif m == 10:
            if m <= month:
                return self.okt_rencana
            elif m > month and self.okt_pengalihan:
                return self.okt_pengalihan
            else:
                return self.okt_rencana
        elif m == 11:
            if m <= month:
                return self.nov_rencana
            elif m > month and self.nov_pengalihan:
                return self.nov_pengalihan
            else:
                return self.nov_rencana
        elif m == 12:
            if m <= month:
                return self.des_rencana
            elif m > month and self.des_pengalihan:
                return self.des_pengalihan
            else:
                return self.des_rencana

    def get_total_realisasi(self):
        return sum([int(self.get_realisasi_month(i)) for i in range(1,13)])
    
    def get_sisa_aki(self):
        return self.real_aki() - self.get_total_realisasi()
    
    def get_usulan(self):
        usulan = UsulanRekomposisiData.objects.filter(prk=self.prk).first()
        return usulan

class Document(models.Model):
    document_number     = models.CharField(max_length=100)
    published_date      = models.DateField()
    upload_date         = models.DateTimeField(auto_now_add=True)
    uploader            = models.ForeignKey(Account, on_delete=models.CASCADE)
    regarding           = models.CharField(max_length=200)
    file                = models.FileField(upload_to='document/skai')

    def __str__(self):
        return self.document_number

class DocSKAI(models.Model):
    document        = models.ForeignKey('Document', on_delete=models.CASCADE, related_name="doc")
    year            = models.IntegerField()
    type            = models.CharField(max_length=50, default="Penetapan")
    keyword         = models.CharField(max_length=100, default="SKAI")
    lrpa_include    = models.BooleanField(default=False)
    
    #Macro
    macro           = models.ForeignKey('Macro', on_delete=models.CASCADE, blank=True, null=True)

    #Macro Document
    macro_doc       = models.FileField(upload_to='document/macro', blank=True, null=True)

    #JSON File
    json            = models.FileField(upload_to='document/json', blank=True, null = True)

    # set up the reverse relation to GenericForeignKey
    notifications   		= GenericRelation(Notification)

    def __str__(self):
        return self.document.regarding
    
    def create_notif_on_upload(self, account, content):
        content_type = ContentType.objects.get_for_model(self)
        
        self.notifications.create(
            target=self,
            from_user=account,
			redirect_url=f"{settings.BASE_URL}",
			verb=f"{account.name} uploaded SKAI. ({content})",
			content_type=content_type,
		)
        self.save()
    
    @property
    def get_cname(self):
        """
		For determining what kind of object is associated with a Notification
		"""
        return "DocSKAI"

class Macro(models.Model):
    macro_file_1        = models.ForeignKey('MacroFile', on_delete=models.CASCADE, related_name="macro_before")
    macro_file_2        = models.ForeignKey('MacroFile', on_delete=models.CASCADE, null=True, blank=True, related_name="macro_after")

class MacroFile(models.Model):
    #uploader            = models.ForeignKey(Account, on_delete=models.CASCADE)
    upload_date         = models.DateTimeField(auto_now_add=True)

class MacroData(models.Model):
    #Based on excel file
    macro_file                  = models.ForeignKey('MacroFile', on_delete=models.CASCADE)
    prk                         = models.ForeignKey('PRK', on_delete=models.CASCADE, blank=True, null=True)
    no_prk                      = models.CharField(max_length=255, blank=True, null=True) #
    no_program                  = models.PositiveIntegerField(blank=True, null=True) #
    no_ruptl                    = models.CharField(max_length=255, blank=True, null=True) #
    cluster                     = models.CharField(max_length=255, blank=True, null=True) #
    fungsi                      = models.CharField(max_length=255, blank=True, null=True) #
    sub_fungsi                  = models.CharField(max_length=255, blank=True, null=True) #
    program_utama               = models.CharField(max_length=255, blank=True, null=True) #
    score                       = models.CharField(max_length=255, blank=True, null=True) #
    jenis_program               = models.CharField(max_length=255, blank=True, null=True) #
    keg_no                      = models.PositiveIntegerField(blank=True, null=True) #
    keg_uraian                  = models.TextField(blank=True, null=True) #
    keg_target_fisik            = models.CharField(max_length=255, blank=True, null=True)
    keg_satuan                  = models.CharField(max_length=255, blank=True, null=True)
    ang_nilai                   = models.FloatField(blank=True, null=True)
    ang_status                  = models.CharField(max_length=255, blank=True, null=True)
    ang_jenis_kontrak           = models.CharField(max_length=255, blank=True, null=True)
    ang_no_kontrak              = models.TextField(blank=True, null=True)
    realisasi_pembayaran        = models.FloatField(blank=True, null=True)
    prediksi_pembayaran         = models.FloatField(blank=True, null=True)
    ai_this_year                = models.FloatField(blank=True, null=True)
    aki_this_year               = models.FloatField(blank=True, null=True)
    aki_n1_year                 = models.FloatField(blank=True, null=True)
    aki_n2_year                 = models.FloatField(blank=True, null=True)
    aki_n3_year                 = models.FloatField(blank=True, null=True)
    aki_n4_year                 = models.FloatField(blank=True, null=True)
    aki_after_n1_year           = models.FloatField(blank=True, null=True)
    sumber_dana                 = models.CharField(max_length=255, blank=True, null=True)
    rencana_terkontrak          = models.CharField(max_length=255, blank=True, null=True)
    rencana_COD                 = models.DateField(blank=True, null=True)
    jan_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    jan_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    feb_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    feb_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    mar_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    mar_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    apr_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    apr_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    mei_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    mei_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    jun_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    jun_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    jul_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    jul_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    aug_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    aug_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    sep_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    sep_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    okt_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    okt_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    nov_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    nov_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)
    des_progress_fisik          = models.CharField(max_length=255,blank=True, null=True)
    des_rencana_disburse        = models.CharField(max_length=255,blank=True, null=True)

    @property
    def real_ai(self):
        return round(self.ai_this_year * 1000)

    @property
    def real_aki(self):
        return round(self.aki_this_year * 1000)
    
    def ai_in_million(self):
        return self.ai_this_year/1000
    
    def aki_in_million(self):
        return self.aki_this_year/1000
    
    def real_nilai_ang(self):
        return round(self.ang_nilai * 1000)
    
    def real_realisasi_pembayaran(self):
        return round(self.realisasi_pembayaran * 1000)

    def real_prediksi_pembayaran(self):
        return round(self.prediksi_pembayaran * 1000)
    
    

    

