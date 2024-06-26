# Generated by Django 5.0.6 on 2024-06-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0006_alter_prom_db_patent_grant_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invention_bd',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='pct_application_examination_start_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='date_of_application_to_wich_additional_data_has_been_received',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='initial_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='initial_application_priority_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='patent_grant_publish_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_examination_start_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_publish_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='previous_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
