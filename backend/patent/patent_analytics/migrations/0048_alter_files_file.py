# Generated by Django 5.0.6 on 2024-06-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0047_alter_files_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.CharField(max_length=500),
        ),
    ]