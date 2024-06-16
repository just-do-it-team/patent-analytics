# Generated by Django 5.0.6 on 2024-06-06 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patent_analytics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invention_bd',
            old_name='crimean_invention_application_date_for_state_registration_in_ukraine',
            new_name='crimean_invention_application_date',
        ),
        migrations.RenameField(
            model_name='invention_bd',
            old_name='crimean_invention_application_number_for_state_registration_in_ukraine',
            new_name='crimean_invention_application_number',
        ),
        migrations.RenameField(
            model_name='invention_bd',
            old_name='information_about_the_obligation_to_conclude_contract_of_alienation',
            new_name='information_about_the_obligation',
        ),
        migrations.RenameField(
            model_name='pmodels_bd',
            old_name='crimean_utility_application_date_for_state_registration_in_ukraine',
            new_name='crimean_utility_application_date',
        ),
        migrations.RenameField(
            model_name='pmodels_bd',
            old_name='crimean_utility_application_number_for_state_registration_in_ukraine',
            new_name='crimean_utility_application_number',
        ),
        migrations.RenameField(
            model_name='prom_db',
            old_name='crimean_industrial_design_application_date_for_state_registration_in_ukraine',
            new_name='crimean_industrial_design_application_date',
        ),
        migrations.RenameField(
            model_name='prom_db',
            old_name='crimean_industrial_design_application_number_for_state_registration_in_ukraine',
            new_name='crimean_industrial_design_application_number',
        ),
        migrations.RenameField(
            model_name='prom_db',
            old_name='industrial_designs_names_and_number_for_which_patent_term_is_prolonged',
            new_name='industrial_designs_names_and_number',
        ),
        migrations.RenameField(
            model_name='prom_db',
            old_name='numbers_of_list_of_essential_features_for_which_patent_term_is_prolonged',
            new_name='numbers_of_list_of_essential_features',
        ),
    ]
