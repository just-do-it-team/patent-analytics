from rest_framework import serializers
from .models import Files, Reports, Invention_bd, PModels_bd , Prom_bd


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'file', 'datetime', 'percent']


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['id', 'datetime', 'invention_bd', 'pmodels_bd', 'prom_bd', 'start_date', 'end_date', 'inn', 'okopf',
                  'okopf_code', 'okfs', 'okfs_code', 'file']


# class

# class Invention_bdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invention_bd
#         fields = ['registration_number', 'registration_date', 'application_number',
#                'application_date', 'authors', 'authors_in_latin', 'patent_holders',
#                'patent_holders_in_latin', 'correspondence_address',
#                'correspondence_address_in_latin', 'invention_name',
#                'patent_starting_date',
#                'crimean_invention_application_number',
#                'crimean_invention_application_date',
#                'crimean_invention_patent_number_in_ukraine',
#                'receipt_date_of_additional_data_to_application',
#                'date_of_application_to_wich_additional_data_has_been_received',
#                'number_of_application_to_wich_additional_data_has_been_received',
#                'initial_application_number', 'initial_application_date',
#                'initial_application_priority_date', 'previous_application_number',
#                'previous_application_date', 'paris_convention_priority_number',
#                'paris_convention_priority_date',
#                'paris_convention_priority_country_code',
#                'pct_application_examination_start_date', 'pct_application_number',
#                'pct_application_date', 'pct_application_publish_number',
#                'pct_application_publish_date', 'ea_application_number',
#                'ea_application_date', 'ea_application_publish_number',
#                'ea_application_publish_date', 'application_publish_date',
#                'application_publish_number', 'patent_grant_publish_date',
#                'patent_grant_publish_number', 'revoked_patent_number',
#                'information_about_the_obligation_to_conclude_contract_of_alienation',
#                'expiration_date',
#                'invention_formula_numbers_for_which_patent_term_is_prolonged',
#                'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47',
#                'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
#                'okopf', 'okopf_code', 'okfs', 'okfs_code']
#
# class PModelsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PModels_bd
#         fields = ['registration_number', 'registration_date', 'application_number',
#               'application_date', 'authors', 'authors_in_latin', 'patent_holders',
#               'patent_holders_in_latin', 'correspondence_address',
#               'correspondence_address_in_latin', 'utility_model_name',
#               'patent_starting_date',
#               'crimean_utility_application_number',
#               'crimean_utility_application_date',
#               'crimean_utility_patent_number_in_ukraine',
#               'receipt_date_of_additional_data_to_application',
#               'date_of_application_to_wich_additional_data_has_been_received',
#               'number_of_application_to_wich_additional_data_has_been_received',
#               'initial_application_number', 'initial_application_date',
#               'initial_application_priority_date', 'previous_application_number',
#               'previous_application_date', 'paris_convention_priority_number',
#               'paris_convention_priority_date',
#               'paris_convention_priority_country_code',
#               'pct_application_examination_start_date', 'pct_application_number',
#               'pct_application_date', 'pct_application_publish_number',
#               'pct_application_publish_date', 'patent_grant_publish_date',
#               'patent_grant_publish_number', 'revoked_patent_number',
#               'expiration_date',
#               'utility_formula_numbers_for_which_patent_term_is_prolonged',
#               'actual', 'publication_URL', 'mpk', 'unnamed_39', 'unnamed_40',
#               'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
#             'okopf', 'okopf_code', 'okfs', 'okfs_code']
#
# class Prom_bdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prom_bd
#         fields = ['registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
#                  'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
#                  'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
#                  'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
#                  'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
#                  'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
#                  'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
#                  'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
#                  'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
#                  'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
#                  'okopf', 'okopf_code', 'okfs', 'okfs_code']