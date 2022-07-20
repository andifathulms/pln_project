# Generated by Django 4.0.6 on 2022-07-20 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dummy', '0002_dummyfileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='dummytable',
            name='dummy_file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='file_parent', to='dummy.dummyfileupload'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dummyfileupload',
            name='notes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
