# Generated by Django 4.0.6 on 2022-08-01 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_delete_docaddedskai'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docskai',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc', to='document.document'),
        ),
    ]
