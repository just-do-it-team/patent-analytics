# Generated by Django 5.0.6 on 2024-06-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0028_alter_orgs_mail_spark_alter_orgs_tel_spark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgs',
            name='principal',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]