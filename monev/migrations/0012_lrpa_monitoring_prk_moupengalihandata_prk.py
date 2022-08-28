# Generated by Django 4.0.6 on 2022-08-28 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0020_macrodata_prk_prk_kode_bpo_prk_kode_prk_and_more'),
        ('monev', '0011_alter_moupengalihandata_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='lrpa_monitoring',
            name='prk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.prk'),
        ),
        migrations.AddField(
            model_name='moupengalihandata',
            name='prk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.prk'),
        ),
    ]
