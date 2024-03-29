# Generated by Django 4.0.6 on 2022-09-02 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('document', '0020_macrodata_prk_prk_kode_bpo_prk_kode_prk_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsulanRekomposisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_date', models.DateTimeField(blank=True, null=True)),
                ('last_edit_date', models.DateTimeField(blank=True, null=True)),
                ('for_month', models.PositiveIntegerField()),
                ('division', models.CharField(blank=True, max_length=10, null=True)),
                ('is_draft', models.BooleanField(default=True)),
                ('is_publish', models.BooleanField(default=False)),
                ('proposed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsulanRekomposisiData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jan', models.IntegerField(blank=True, null=True)),
                ('feb', models.IntegerField(blank=True, null=True)),
                ('mar', models.IntegerField(blank=True, null=True)),
                ('apr', models.IntegerField(blank=True, null=True)),
                ('mei', models.IntegerField(blank=True, null=True)),
                ('jun', models.IntegerField(blank=True, null=True)),
                ('jul', models.IntegerField(blank=True, null=True)),
                ('aug', models.IntegerField(blank=True, null=True)),
                ('sep', models.IntegerField(blank=True, null=True)),
                ('okt', models.IntegerField(blank=True, null=True)),
                ('nov', models.IntegerField(blank=True, null=True)),
                ('des', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recomposition.usulanrekomposisi')),
                ('prk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.prk')),
            ],
        ),
    ]
