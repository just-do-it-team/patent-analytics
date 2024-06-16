# def prom_bd_values():
#     columns = ['registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
#                                              'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
#                                              'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
#                                              'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
#                                              'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
#                                              'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
#                                              'previous_application_number', 'previous_application_date',
#                                              'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
#                                              'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
#                                              'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
#                                              'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
#                                              'okopf', 'okopf_code', 'okfs', 'okfs_code']
#     return columns


def prom_bd_excel():
    columns = ['registration number', 'registration date', 'application number', 'application_date', 'authors', 'authors in latin', 'patent holders',
                'patent holders in latin', 'correspondence address', 'correspondence address in latin', 'industrial design name', 'patent starting date',
                'Crimean industrial design application number for state registration in Ukraine', 'Crimean industrial design application date for state registration in Ukraine',
                'Crimean industrial design patent number in Ukraine', 'receipt date of additional data to application',
                'date of application to which additional data has been received', 'number of application to which additional data has been received',
                'initial application number', 'initial application date', 'initial application priority date',
               'previous application number', 'previous application date', 'paris convention priority number', 'paris convention priority date', 'paris convention priority country code', 'patent grant publish date',
                'patent grant publish number', 'revoked patent number', 'expiration date',
                 'numbers of list of essential features for which patent term is prolonged', 'industrial designs names and number for which patent term is prolonged',
                 'actual', 'publication URL', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                 'okopf', 'okopf_code', 'okfs', 'okfs_code']
    return columns

# def invention_bd_values():
#     columns = ['registration_number', 'registration_date', 'application_number',
#                                                'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
#                                                'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
#                                                'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
#                                                'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
#                                                'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
#                                                'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
#                                                'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
#                                                'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
#                                                'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
#                                                'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
#                                                'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
#                                                 'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code']
#     return columns

def invention_bd_excel():
    columns = ['registration number', 'registration date', 'application number',
       'application date', 'authors', 'authors in latin', 'patent holders',
       'patent holders in latin', 'correspondence address',
       'correspondence address in latin', 'invention name',
       'patent starting date',
       'Crimean invention application number for state registration in Ukraine',
       'Crimean invention application date for state registration in Ukraine',
       'Crimean invention patent number in Ukraine',
       'receipt date of additional data to application',
       'date of application to which additional data has been received',
       'number of application to which additional data has been received',
       'initial application number', 'initial application date',
       'initial application priority date', 'previous application number',
       'previous application date', 'paris convention priority number',
       'paris convention priority date',
       'paris convention priority country code',
       'PCT application examination start date', 'PCT application number',
       'PCT application date', 'PCT application publish number',
       'PCT application publish date', 'EA application number',
       'EA application date', 'EA application publish number',
       'EA application publish date', 'application publish date',
       'application publish number', 'patent grant publish date',
       'patent grant publish number', 'revoked patent number',
       'information about the obligation to conclude contract of alienation',
       'expiration date',
       'invention formula numbers for which patent term is prolonged',
       'additional patent', 'actual', 'mpk', 'Unnamed: 46', 'Unnamed: 47',
       'Unnamed: 48', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
       'okopf', 'okopf_code', 'okfs', 'okfs_code']
    return columns


# def pmodels_bd_values():
#    columns = ['registration_number',
#                 'registration_date',
#                 'application_number',
#                 'application_date', 'authors',
#                 'authors_latin', 'patent_holders',
#                 'patent_holders_latin',
#                 'correspondence_address',
#                 'correspondence_address_latin',
#                 'utility_model_name',
#                 'patent_starting_date',
#                 'crimean_utility_application_number',
#                 'crimean_utility_application_date',
#                 'crimean_utility_patent_number_in_ukraine',
#                 'receipt_date_of_additional_data_to_application',
#                 'date_of_application_to_wich_additional_data_has_been_received',
#                 'number_of_application_to_wich_additional_data_has_been_received',
#                 'initial_application_number',
#                 'initial_application_date',
#                 'initial_application_priority_date',
#                 'previous_application_number',
#                 'previous_application_date',
#                 'paris_convention_priority_number',
#                 'paris_convention_priority_date',
#                 'paris_convention_priority_country',
#                 'pct_application_examination_start_date',
#                 'pct_application_number',
#                 'pct_application_date',
#                 'pct_application_publish_number',
#                 'pct_application_publish_date',
#                 'patent_grant_publish_date',
#                 'patent_grant_publish_number',
#                 'revoke_patent_number',
#                 'expiration_date',
#                 'utility_formula_numbers_for_which_patent_term_is_prolonged',
#                 'actual', 'publication_url', 'mpk',
#                 'unnamed_39', 'unnamed_40',
#                 'head_or_branch', 'id_child', 'inn',
#                 'is_active', 'ogrn',
#                 'okopf', 'okopf_code', 'okfs',
#                 'okfs_code']
#    return columns


def pmodels_bd_excel():
    columns = ['registration number', 'registration date', 'application number',
       'application date', 'authors', 'authors in latin', 'patent holders',
       'patent holders in latin', 'correspondence address',
       'correspondence address in latin', 'utility model name',
       'patent starting date',
       'Crimean utility model application number for state registration in Ukraine',
       'Crimean utility model application date for state registration in Ukraine',
       'Crimean utility model patent number in Ukraine',
       'receipt date of additional data to application',
       'date of application to which additional data has been received',
       'number of application to which additional data has been received',
       'initial application number', 'initial application date',
       'initial application priority date', 'previous application number',
       'previous application date', 'paris convention priority number',
       'paris convention priority date',
       'paris convention priority country code',
       'PCT application examination start date', 'PCT application number',
       'PCT application date', 'PCT application publish number',
       'PCT application publish date', 'patent grant publish date',
       'patent grant publish number', 'revoked patent number',
       'expiration date',
       'utility model formula numbers for which patent term is prolonged',
       'actual', 'publication URL', 'mpk', 'Unnamed: 39', 'Unnamed: 40',
        'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
       'okopf', 'okopf_code', 'okfs', 'okfs_code']
    return columns

def inv_and_pmodels():
    columns = ['patent_starting_date', 'ea_application_publish_date', 'okopf', 'inn', 'ogrn', 'patent_grant_publish_number', 'authors_latin', 'crimean_invention_application_date', 'initial_application_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged', 'patent_holders', 'initial_application_priority_date', 'unnamed_47', 'utility_formula_numbers_for_which_patent_term_is_prolonged', 'patent_holders_latin', 'previous_application_number', 'crimean_invention_application_number', 'pct_application_publish_number', 'receipt_date_of_additional_data_to_application', 'actual', 'application_publish_number', 'number_of_application_to_wich_additional_data_has_been_received', 'revoke_patent_number', 'correspondence_address_latin', 'paris_convention_priority_date', 'crimean_utility_application_number', 'ea_application_number', 'unnamed_46', 'correspondence_address', 'unnamed_40', 'crimean_invention_patent_number_in_ukraine', 'information_about_the_obligation', 'unnamed_48', 'initial_application_number', 'pct_application_publish_date', 'paris_convention_priority_country', 'crimean_utility_patent_number_in_ukraine', 'registration_number', 'date_of_application_to_wich_additional_data_has_been_received', 'mpk', 'expiration_date', 'ea_application_date', 'registration_date', 'invention_name', 'okopf_code', 'application_number', 'paris_convention_priority_number', 'publication_url', 'pct_application_date', 'crimean_utility_application_date', 'head_or_branch', 'id_child', 'application_publish_date', 'pct_application_number', 'application_date', 'pct_application_examination_start_date', 'authors', 'okfs_code', 'okfs', 'patent_grant_publish_date', 'additional_patent', 'is_active', 'unnamed_39', 'previous_application_date', 'ea_application_publish_number', 'utility_model_name']
    return columns

# def pmodels