# Generated by Django 5.0.6 on 2024-06-08 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0032_alter_prom_bd_paris_convention_priority_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prom_bd',
            name='industrial_design_name',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]
