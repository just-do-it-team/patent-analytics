# Generated by Django 5.0.6 on 2024-06-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0025_rename_egrul_status_orgs_egrul_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgs',
            name='mail_SPARK',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
