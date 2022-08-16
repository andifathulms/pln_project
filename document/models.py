from django.db import models
from account.models import Account

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from notification.models import Notification

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
    no_prk                      = models.CharField(max_length=100, blank=True, null=True)
    no_program                  = models.PositiveIntegerField(blank=True, null=True)
    no_ruptl                    = models.CharField(max_length=100, blank=True, null=True)
    cluster                     = models.CharField(max_length=100, blank=True, null=True)
    fungsi                      = models.CharField(max_length=100, blank=True, null=True)
    sub_fungsi                  = models.CharField(max_length=100, blank=True, null=True)
    program_utama               = models.CharField(max_length=100, blank=True, null=True)
    score                       = models.CharField(max_length=5, blank=True, null=True)
    jenis_program               = models.CharField(max_length=100, blank=True, null=True)
    keg_no                      = models.PositiveIntegerField(blank=True, null=True)
    keg_uraian                  = models.TextField(blank=True, null=True)
    keg_target_fisik            = models.CharField(max_length=10, blank=True, null=True)
    keg_satuan                  = models.CharField(max_length=10, blank=True, null=True)
    ang_nilai                   = models.IntegerField(blank=True, null=True)
    ang_status                  = models.CharField(max_length=100, blank=True, null=True)
    ang_jenis_kontrak           = models.CharField(max_length=100, blank=True, null=True)
    ang_no_kontrak              = models.CharField(max_length=200, blank=True, null=True)
    realisasi_pembayaran        = models.IntegerField(blank=True, null=True)
    prediksi_pembayaran         = models.IntegerField(blank=True, null=True)
    ai_this_year                = models.IntegerField(blank=True, null=True) #Try use FloatField
    aki_this_year               = models.IntegerField(blank=True, null=True) #Try use FloatField
    aki_n1_year                 = models.IntegerField(blank=True, null=True)
    aki_n2_year                 = models.IntegerField(blank=True, null=True)
    aki_n3_year                 = models.IntegerField(blank=True, null=True)
    aki_n4_year                 = models.IntegerField(blank=True, null=True)
    aki_after_n1_year           = models.IntegerField(blank=True, null=True)
    sumber_dana                 = models.CharField(max_length=100, blank=True, null=True)
    rencana_terkontrak          = models.CharField(max_length=50, blank=True, null=True)
    rencana_COD                 = models.DateField(blank=True, null=True)
    jan_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    jan_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    feb_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    feb_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    mar_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    mar_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    apr_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    apr_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    mei_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    mei_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    jun_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    jun_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    jul_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    jul_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    aug_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    aug_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    sep_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    sep_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    okt_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    okt_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    nov_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    nov_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)
    des_progress_fisik          = models.CharField(max_length=100,blank=True, null=True)
    des_rencana_disburse        = models.CharField(max_length=100,blank=True, null=True)

    def real_ai(self):
        return self.ai_this_year * 1000

    def real_aki(self):
        return self.aki_this_year * 1000

