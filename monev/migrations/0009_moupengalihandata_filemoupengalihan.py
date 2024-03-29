# Generated by Django 4.0.6 on 2022-08-23 12:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monev', '0008_prk_lookup_upp'),
    ]

    operations = [
        migrations.CreateModel(
            name='MouPengalihanData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_prk', models.CharField(blank=True, max_length=100, null=True)),
                ('mou', models.CharField(blank=True, max_length=255, null=True)),
                ('ai_this_year', models.FloatField(blank=True, null=True)),
                ('aki_this_year', models.FloatField(blank=True, null=True)),
                ('jan', models.CharField(blank=True, max_length=100, null=True)),
                ('feb', models.CharField(blank=True, max_length=100, null=True)),
                ('mar', models.CharField(blank=True, max_length=100, null=True)),
                ('apr', models.CharField(blank=True, max_length=100, null=True)),
                ('mei', models.CharField(blank=True, max_length=100, null=True)),
                ('jun', models.CharField(blank=True, max_length=100, null=True)),
                ('jul', models.CharField(blank=True, max_length=100, null=True)),
                ('aug', models.CharField(blank=True, max_length=100, null=True)),
                ('sep', models.CharField(blank=True, max_length=100, null=True)),
                ('okt', models.CharField(blank=True, max_length=100, null=True)),
                ('nov', models.CharField(blank=True, max_length=100, null=True)),
                ('des', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monev.lrpa_file')),
            ],
        ),
        migrations.CreateModel(
            name='FileMouPengalihan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='monev/mou_pengalihan')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('file_export_date', models.DateField(default=datetime.date.today)),
                ('for_month', models.IntegerField()),
                ('for_year', models.IntegerField()),
                ('upload_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
