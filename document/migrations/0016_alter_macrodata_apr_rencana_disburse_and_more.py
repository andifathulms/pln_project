# Generated by Django 4.0.6 on 2022-08-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0015_alter_macrodata_apr_progress_fisik_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macrodata',
            name='apr_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='aug_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='des_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='feb_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='jan_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='jul_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='jun_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='mar_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='mei_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='nov_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='okt_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='macrodata',
            name='sep_rencana_disburse',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
