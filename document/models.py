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
    revision        = models.BooleanField(default=False)
    revision_number = models.PositiveIntegerField(blank=True, null=True)

    #Macro
    macro           = models.ForeignKey('Macro', on_delete=models.CASCADE, blank=True, null=True)
    #Macro Doc later

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
        print("DONE")
    
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
    uploader            = models.ForeignKey(Account, on_delete=models.CASCADE)
    upload_date         = models.DateTimeField(auto_now_add=True)

class MacroData(models.Model):
    #Based on excel file
    macro_file              = models.ForeignKey('MacroFile', on_delete=models.CASCADE)
    no_prk                  = models.CharField(max_length=100)
    no_program              = models.PositiveIntegerField()
    no_ruptl                = models.CharField(max_length=100)
    cluster                 = models.CharField(max_length=100)
    fungsi                  = models.CharField(max_length=100)
    sub_fungsi              = models.CharField(max_length=100)
    program_utama           = models.CharField(max_length=100)
    score                   = models.CharField(max_length=5)
    jenis_program           = models.CharField(max_length=100)
    keg_no                  = models.PositiveIntegerField()
    keg_uraian              = models.TextField()
    keg_target_fisik        = models.CharField(max_length=10)
    keg_satuan              = models.CharField(max_length=10)
    ang_nilai               = models.IntegerField()
    ang_status              = models.CharField(max_length=100)
    ang_jenis_kontrak       = models.CharField(max_length=100)
    ang_no_kontrak          = models.CharField(max_length=200)
    realisasi_pembayaran    = models.IntegerField()
    prediksi_pembayaran     = models.IntegerField()
    ai_this_year            = models.IntegerField()
    aki_this_year           = models.IntegerField()
    aki_n1_year             = models.IntegerField()
    aki_n2_year             = models.IntegerField()
    aki_n3_year             = models.IntegerField()
    aki_n4_year             = models.IntegerField()
    aki_after_n1_year       = models.IntegerField()
    sumber_dana             = models.CharField(max_length=100)


