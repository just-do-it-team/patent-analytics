# Generated by Django 5.0.6 on 2024-06-07 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0012_alter_orgs_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgs',
            name='OKVAD2_add',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
