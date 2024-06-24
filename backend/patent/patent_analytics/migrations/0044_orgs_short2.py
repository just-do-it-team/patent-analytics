# Generated by Django 5.0.6 on 2024-06-09 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0043_remove_orgs_short_creation_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orgs_short2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_company', models.IntegerField(blank=True, null=True)),
                ('full_name', models.CharField(blank=True, max_length=500, null=True)),
                ('short_name', models.CharField(blank=True, max_length=500, null=True)),
                ('inn', models.CharField(blank=True, max_length=20, null=True)),
                ('ogrn', models.CharField(blank=True, max_length=20, null=True)),
                ('head_or_branch', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('okopf_code', models.CharField(blank=True, max_length=50, null=True)),
                ('okopf', models.CharField(blank=True, max_length=500, null=True)),
                ('okfs_code', models.CharField(blank=True, max_length=50, null=True)),
                ('okfs', models.CharField(blank=True, max_length=500, null=True)),
                ('is_active', models.CharField(blank=True, max_length=10, null=True)),
                ('id_child', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]