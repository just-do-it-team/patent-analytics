# Generated by Django 5.0.6 on 2024-06-07 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0011_alter_orgs_creation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgs',
            name='is_active',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
