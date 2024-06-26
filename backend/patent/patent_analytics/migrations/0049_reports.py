# Generated by Django 5.0.6 on 2024-06-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0048_alter_files_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('invention_bd', models.BooleanField()),
                ('pmodels_bd', models.BooleanField()),
                ('prom_bd', models.BooleanField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('inn', models.CharField(blank=True, max_length=10000, null=True)),
                ('okopf', models.CharField(blank=True, max_length=10000, null=True)),
                ('okopf_code', models.CharField(blank=True, max_length=10000, null=True)),
                ('okfs', models.CharField(blank=True, max_length=10000, null=True)),
                ('okfs_code', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
    ]
