# Generated by Django 4.0.6 on 2022-09-06 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monev', '0012_lrpa_monitoring_prk_moupengalihandata_prk'),
        ('document', '0020_macrodata_prk_prk_kode_bpo_prk_kode_prk_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PRKData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prk_data_year', models.PositiveIntegerField(default=2022)),
                ('disburse_year_before', models.CharField(blank=True, max_length=100, null=True)),
                ('mekanisme_pembayaran', models.CharField(blank=True, max_length=100, null=True)),
                ('jan_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('jan_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('feb_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('feb_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('mar_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('mar_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('apr_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('apr_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('mei_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('mei_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('jun_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('jun_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('jul_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('jul_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('aug_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('aug_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('sep_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('sep_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('okt_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('okt_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('nov_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('nov_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('des_rencana', models.CharField(blank=True, max_length=100, null=True)),
                ('des_realisasi', models.CharField(blank=True, max_length=100, null=True)),
                ('ai_this_year', models.FloatField(blank=True, null=True)),
                ('aki_this_year', models.FloatField(blank=True, null=True)),
                ('mou', models.CharField(blank=True, max_length=255, null=True)),
                ('jan_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('feb_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('mar_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('apr_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('mei_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('jun_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('jul_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('aug_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('sep_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('okt_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('nov_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('des_pengalihan', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monev.filemoupengalihan')),
                ('file_lrpa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monev.lrpa_file')),
                ('prk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.prk')),
            ],
        ),
    ]