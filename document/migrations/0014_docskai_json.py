# Generated by Django 4.0.6 on 2022-08-08 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0013_macrodata_apr_progress_fisik_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='docskai',
            name='json',
            field=models.FileField(blank=True, null=True, upload_to='document/json'),
        ),
    ]
