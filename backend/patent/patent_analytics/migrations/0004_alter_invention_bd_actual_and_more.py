# Generated by Django 5.0.6 on 2024-06-06 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0003_alter_invention_bd_actual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invention_bd',
            name='actual',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='additional_patent',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='application_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='application_publish_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='application_publish_number',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='authors',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='authors_latin',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='correspondence_address',
            field=models.CharField(blank=True, max_length=5500, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='correspondence_address_latin',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='crimean_invention_application_date',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='crimean_invention_application_number',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='crimean_invention_patent_number_in_ukraine',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='date_of_application_to_wich_additional_data_has_been_received',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='ea_application_date',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='ea_application_number',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='ea_application_publish_date',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='ea_application_publish_number',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='expiration_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='information_about_the_obligation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='initial_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='initial_application_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='initial_application_priority_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='invention_formula_numbers_for_which_patent_term_is_prolonged',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='invention_name',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='mpk',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='number_of_application_to_wich_additional_data_has_been_received',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='paris_convention_priority_country',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='paris_convention_priority_date',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='paris_convention_priority_number',
            field=models.CharField(blank=True, max_length=1700, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='patent_grant_publish_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='patent_grant_publish_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='patent_holders',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='patent_holders_latin',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='patent_starting_date',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='pct_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='pct_application_examination_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='pct_application_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='pct_application_publish_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='pct_application_publish_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='previous_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='previous_application_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='receipt_date_of_additional_data_to_application',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='registration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='registration_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='revoke_patent_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='unnamed_46',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='unnamed_47',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='invention_bd',
            name='unnamed_48',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='actual',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='application_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='application_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='authors',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='authors_latin',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='correspondence_address',
            field=models.CharField(blank=True, max_length=5500, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='correspondence_address_latin',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='crimean_utility_application_date',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='crimean_utility_application_number',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='crimean_utility_patent_number_in_ukraine',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='date_of_application_to_wich_additional_data_has_been_received',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='initial_application_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='initial_application_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='initial_application_priority_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='mpk',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='number_of_application_to_wich_additional_data_has_been_received',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='paris_convention_priority_country',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='paris_convention_priority_date',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='paris_convention_priority_number',
            field=models.CharField(blank=True, max_length=1700, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='patent_grant_publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='patent_grant_publish_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='patent_holders',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='patent_holders_latin',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='patent_starting_date',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_examination_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='pct_application_publish_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='previous_application_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='previous_application_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='publication_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='receipt_date_of_additional_data_to_application',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='registration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='registration_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='revoke_patent_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='unnamed_39',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='unnamed_40',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='utility_formula_numbers_for_which_patent_term_is_prolonged',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pmodels_bd',
            name='utility_model_name',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='actual',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='application_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='application_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='authors',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='authors_latin',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='correspondence_address',
            field=models.CharField(blank=True, max_length=5500, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='correspondence_address_latin',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='crimean_industrial_design_application_date',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='crimean_industrial_design_application_number',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='crimean_industrial_design_patent_number_in_ukraine',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='date_of_application_to_wich_additional_data_has_been_received',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='expiration_date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='industrial_design_name',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='industrial_designs_names_and_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='initial_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='initial_application_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='initial_application_priority_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='number_of_application_to_wich_additional_data_has_been_received',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='numbers_of_list_of_essential_features',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='paris_convention_priority_country',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='paris_convention_priority_date',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='paris_convention_priority_number',
            field=models.CharField(blank=True, max_length=1700, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='patent_grant_publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='patent_grant_publish_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='patent_holders',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='patent_holders_latin',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='patent_starting_date',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='previous_application_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='previous_application_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='publication_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='receipt_date_of_additional_data_to_application',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='registration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='registration_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prom_db',
            name='revoke_patent_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
