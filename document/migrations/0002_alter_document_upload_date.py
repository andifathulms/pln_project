# Generated by Django 4.0.6 on 2022-07-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]