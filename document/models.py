from django.db import models
from account.models import Account

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
    document        = models.ForeignKey('Document', on_delete=models.CASCADE)
    year            = models.IntegerField()
    revision        = models.BooleanField()
    revision_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.revision:
            return "SKAI " + str(self.year) + " Revisi - " + str(self.revision_number)
        return "SKAI " + str(self.year)
    
class DocAddedSKAI(models.Model):
    document        = models.ForeignKey('Document', on_delete=models.CASCADE)
    revision_on     = models.ForeignKey('DocSKAI', on_delete=models.CASCADE)
    revision_number = models.PositiveIntegerField()

    def __str__(self):
        return "Tambahan AI/AKI atas " + self.revision_on.__str__()
    
