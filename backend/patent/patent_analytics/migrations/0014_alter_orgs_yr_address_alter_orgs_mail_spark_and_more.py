# Generated by Django 5.0.6 on 2024-06-07 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0013_alter_orgs_okvad2_add'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgs',
            name='Yr_address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='orgs',
            name='mail_SPARK',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='orgs',
            name='real_address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='orgs',
            name='short_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]