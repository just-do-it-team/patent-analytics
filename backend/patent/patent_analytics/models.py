from django.db import models


class Orgs_short2(models.Model):
    id_company = models.IntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    inn = models.CharField(max_length=20, blank=True, null=True)
    ogrn = models.CharField(max_length=20, blank=True, null=True)
    head_or_branch = models.PositiveSmallIntegerField(blank=True, null=True)
    okopf_code = models.CharField(max_length=50, blank=True, null=True) #
    okopf = models.CharField(max_length=500, blank=True, null=True) #
    okfs_code = models.CharField(max_length=50, blank=True, null=True) #
    okfs = models.CharField(max_length=500, blank=True, null=True) #
    is_active = models.CharField(max_length=10, blank=True, null=True)
    id_child = models.CharField(max_length=100, blank=True, null=True)


class Invention_bd(models.Model):
    registration_number = models.CharField(max_length=12, blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    application_number = models.CharField(max_length=13, blank=True, null=True)
    application_date = models.CharField(max_length=10, blank=True, null=True)
    authors = models.CharField(max_length=3000, blank=True, null=True)
    authors_latin = models.CharField(max_length=3000, blank=True, null=True)
    patent_holders = models.CharField(max_length=1500, blank=True, null=True)
    patent_holders_latin = models.CharField(max_length=700, blank=True, null=True)
    correspondence_address = models.CharField(max_length=5500, blank=True, null=True)
    correspondence_address_latin = models.CharField(max_length=1100, blank=True, null=True)
    invention_name = models.CharField(max_length=1100, blank=True, null=True)
    patent_starting_date = models.CharField(max_length=120, blank=True, null=True)
    crimean_invention_application_number = models.CharField(max_length=60, blank=True, null=True)
    crimean_invention_application_date = models.CharField(max_length=70, blank=True, null=True)
    crimean_invention_patent_number_in_ukraine = models.CharField(max_length=10, blank=True, null=True)
    receipt_date_of_additional_data_to_application = models.CharField(max_length=10, blank=True, null=True)  #дата поступления дополнительных данных к заявке
    date_of_application_to_wich_additional_data_has_been_received = models.CharField(max_length=10, blank=True, null=True)  #дата обращения, к которому получены дополнительные данные
    number_of_application_to_wich_additional_data_has_been_received = models.CharField(max_length=13, blank=True, null=True)  #номер приложения, на которое были получены дополнительные данные
    initial_application_number = models.CharField(max_length=13, blank=True, null=True)
    initial_application_date = models.CharField(max_length=10, blank=True, null=True)
    initial_application_priority_date = models.CharField(max_length=10, blank=True, null=True)  #дата приоритета?? первоначальной заявки
    previous_application_number = models.CharField(max_length=20, blank=True, null=True)
    previous_application_date = models.CharField(max_length=20, blank=True, null=True)
    paris_convention_priority_number = models.CharField(max_length=1700, blank=True, null=True)  #Приоритетный номер Парижской конвенции???
    paris_convention_priority_date = models.CharField(max_length=60, blank=True, null=True)
    paris_convention_priority_country = models.CharField(max_length=350, blank=True, null=True)
    pct_application_examination_start_date = models.CharField(max_length=10, blank=True, null=True)
    pct_application_number = models.CharField(max_length=20, blank=True, null=True)
    pct_application_date = models.CharField(max_length=10, blank=True, null=True)
    pct_application_publish_number = models.CharField(max_length=16, blank=True, null=True)
    pct_application_publish_date = models.CharField(max_length=10, blank=True, null=True)
    ea_application_number = models.CharField(max_length=3, blank=True, null=True)
    ea_application_date = models.CharField(max_length=3, blank=True, null=True)
    ea_application_publish_number = models.CharField(max_length=3, blank=True, null=True)
    ea_application_publish_date = models.CharField(max_length=3, blank=True, null=True)
    application_publish_date = models.CharField(max_length=10, blank=True, null=True)
    application_publish_number = models.CharField(max_length=3, blank=True, null=True)
    patent_grant_publish_date = models.CharField(max_length=10, blank=True, null=True)
    patent_grant_publish_number = models.CharField(max_length=10, blank=True, null=True)
    revoke_patent_number = models.CharField(max_length=10, blank=True, null=True)  #номер аннулированного патента
    information_about_the_obligation = models.CharField(max_length=500, blank=True, null=True)  #сведения об обязательстве по заключению договора отчуждения
    expiration_date = models.DateTimeField(blank=True, null=True)
    invention_formula_numbers_for_which_patent_term_is_prolonged = models.CharField(max_length=100, blank=True, null=True)  #номера формул изобретений, на которые продлевается срок действия патента
    additional_patent = models.CharField(max_length=5, blank=True, null=True)
    actual = models.CharField(max_length=5, blank=True, null=True)
    mpk = models.CharField(max_length=900, blank=True, null=True)
    unnamed_46 = models.CharField(max_length=30, blank=True, null=True)
    unnamed_47 = models.CharField(max_length=30, blank=True, null=True)
    unnamed_48 = models.CharField(max_length=30, blank=True, null=True)
    inn = models.CharField(max_length=20, blank=True, null=True)
    ogrn = models.CharField(max_length=20, blank=True, null=True)
    head_or_branch = models.PositiveSmallIntegerField(blank=True, null=True)
    okopf_code = models.CharField(max_length=50, blank=True, null=True) #
    okopf = models.CharField(max_length=500, blank=True, null=True) #
    okfs_code = models.CharField(max_length=50, blank=True, null=True) #
    okfs = models.CharField(max_length=500, blank=True, null=True) #
    is_active = models.CharField(max_length=10, blank=True, null=True)
    id_child = models.CharField(max_length=100, blank=True, null=True)
    individual = models.CharField(max_length=100, blank=True, null=True)

class PModels_bd(models.Model):
    registration_number = models.CharField(max_length=10, blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    application_number = models.CharField(max_length=13, blank=True, null=True)
    application_date = models.CharField(max_length=10, blank=True, null=True)
    authors = models.CharField(max_length=3000, blank=True, null=True)
    authors_latin = models.CharField(max_length=3000, blank=True, null=True)
    patent_holders = models.CharField(max_length=1500, blank=True, null=True)
    patent_holders_latin = models.CharField(max_length=700, blank=True, null=True)
    correspondence_address = models.CharField(max_length=5500, blank=True, null=True)
    correspondence_address_latin = models.CharField(max_length=1100, blank=True, null=True)
    utility_model_name = models.CharField(max_length=1100, blank=True, null=True)
    patent_starting_date = models.CharField(max_length=120, blank=True, null=True)
    crimean_utility_application_number = models.CharField(max_length=60, blank=True, null=True)
    crimean_utility_application_date = models.CharField(max_length=70, blank=True, null=True)
    crimean_utility_patent_number_in_ukraine = models.CharField(max_length=10, blank=True, null=True)
    receipt_date_of_additional_data_to_application = models.CharField(max_length=20, blank=True, null=True)  # дата поступления дополнительных данных к заявке
    date_of_application_to_wich_additional_data_has_been_received = models.CharField(max_length=10, blank=True, null=True)  # дата обращения, к которому получены дополнительные данные
    number_of_application_to_wich_additional_data_has_been_received = models.CharField(max_length=13, blank=True, null=True)  # номер приложения, на которое были получены дополнительные данные
    initial_application_number = models.CharField(max_length=13, blank=True, null=True)
    initial_application_date = models.CharField(max_length=10, blank=True, null=True)
    initial_application_priority_date = models.CharField(max_length=10, blank=True, null=True)  # дата приоритета?? первоначальной заявки
    previous_application_number = models.CharField(max_length=20, blank=True, null=True)
    previous_application_date = models.CharField(max_length=10, blank=True, null=True)
    paris_convention_priority_number = models.CharField(max_length=1700, blank=True, null=True)  # Приоритетный номер Парижской конвенции???
    paris_convention_priority_date = models.CharField(max_length=60, blank=True, null=True)
    paris_convention_priority_country = models.CharField(max_length=350, blank=True, null=True)
    pct_application_examination_start_date = models.CharField(max_length=10, blank=True, null=True)
    pct_application_number = models.CharField(max_length=20, blank=True, null=True)
    pct_application_date = models.CharField(max_length=10, blank=True, null=True)
    pct_application_publish_number = models.CharField(max_length=16, blank=True, null=True)
    pct_application_publish_date = models.CharField(max_length=10, blank=True, null=True)
    patent_grant_publish_date = models.CharField(max_length=10, blank=True, null=True)
    patent_grant_publish_number = models.CharField(max_length=10, blank=True, null=True)
    revoke_patent_number = models.CharField(max_length=10, blank=True, null=True)  # номер аннулированного патента
    expiration_date = models.DateTimeField(blank=True, null=True)
    utility_formula_numbers_for_which_patent_term_is_prolonged = models.CharField(max_length=100, blank=True, null=True)  # номера формул изобретений, на которые продлевается срок действия патента
    actual = models.CharField(max_length=5, blank=True, null=True)
    publication_url = models.CharField(max_length=200, blank=True, null=True)
    mpk = models.CharField(max_length=900, blank=True, null=True)
    unnamed_39 = models.CharField(max_length=30, blank=True, null=True)
    unnamed_40 = models.CharField(max_length=30, blank=True, null=True)
    inn = models.CharField(max_length=20, blank=True, null=True)
    ogrn = models.CharField(max_length=20, blank=True, null=True)
    head_or_branch = models.PositiveSmallIntegerField(blank=True, null=True)
    okopf_code = models.CharField(max_length=50, blank=True, null=True) #
    okopf = models.CharField(max_length=500, blank=True, null=True) #
    okfs_code = models.CharField(max_length=50, blank=True, null=True) #
    okfs = models.CharField(max_length=500, blank=True, null=True) #
    is_active = models.CharField(max_length=10, blank=True, null=True)
    id_child = models.CharField(max_length=100, blank=True, null=True)
    individual = models.CharField(max_length=100, blank=True, null=True)

class Prom_bd(models.Model):
    registration_number = models.CharField(max_length=10, blank=True, null=True)
    registration_date = models.CharField(max_length=13, blank=True, null=True)
    application_number = models.CharField(max_length=13, blank=True, null=True)
    application_date = models.CharField(max_length=10, blank=True, null=True)
    authors = models.CharField(max_length=1000, blank=True, null=True)
    authors_latin = models.CharField(max_length=1000, blank=True, null=True)
    patent_holders = models.CharField(max_length=1500, blank=True, null=True)
    patent_holders_latin = models.CharField(max_length=700, blank=True, null=True)
    correspondence_address = models.CharField(max_length=1000, blank=True, null=True)
    correspondence_address_latin = models.CharField(max_length=1100, blank=True, null=True)
    industrial_design_name = models.CharField(max_length=1900, blank=True, null=True)
    patent_starting_date = models.CharField(max_length=120, blank=True, null=True)
    crimean_industrial_design_application_number = models.CharField(max_length=60, blank=True, null=True)
    crimean_industrial_design_application_date = models.CharField(max_length=70, blank=True, null=True)
    crimean_industrial_design_patent_number_in_ukraine = models.CharField(max_length=10, blank=True, null=True)
    receipt_date_of_additional_data_to_application = models.CharField(max_length=20, blank=True, null=True)  # дата поступления дополнительных данных к заявке
    date_of_application_to_wich_additional_data_has_been_received = models.CharField(max_length=20, blank=True, null=True)  # дата обращения, к которому получены дополнительные данные
    number_of_application_to_wich_additional_data_has_been_received = models.CharField(max_length=13, blank=True, null=True)  # номер приложения, на которое были получены дополнительные данные
    initial_application_number = models.CharField(max_length=13, blank=True, null=True)
    initial_application_date = models.CharField(max_length=10, blank=True, null=True)
    initial_application_priority_date = models.CharField(max_length=10, blank=True, null=True)  # дата приоритета?? первоначальной заявки
    previous_application_number = models.CharField(max_length=20, blank=True, null=True)
    previous_application_date = models.CharField(max_length=10, blank=True, null=True)
    paris_convention_priority_number = models.CharField(max_length=700, blank=True, null=True)  # Приоритетный номер Парижской конвенции???
    paris_convention_priority_date = models.CharField(max_length=600, blank=True, null=True)
    paris_convention_priority_country = models.CharField(max_length=350, blank=True, null=True)
    patent_grant_publish_date = models.CharField(max_length=10, blank=True, null=True)
    patent_grant_publish_number = models.CharField(max_length=10, blank=True, null=True)
    revoke_patent_number = models.CharField(max_length=10, blank=True, null=True)  # номер аннулированного патента
    expiration_date = models.CharField(max_length=12, blank=True, null=True)
    numbers_of_list_of_essential_features = models.CharField(max_length=10, blank=True, null=True)
    industrial_designs_names_and_number = models.CharField(max_length=10, blank=True, null=True)
    actual = models.CharField(max_length=70, blank=True, null=True)
    publication_url = models.CharField(max_length=200, blank=True, null=True)
    actual_date = models.CharField(max_length=100, blank=True, null=True)
    mkpo = models.CharField(max_length=100, blank=True, null=True)
    inn = models.CharField(max_length=20, blank=True, null=True)
    ogrn = models.CharField(max_length=20, blank=True, null=True)
    head_or_branch = models.PositiveSmallIntegerField(blank=True, null=True)
    okopf_code = models.CharField(max_length=50, blank=True, null=True) #
    okopf = models.CharField(max_length=500, blank=True, null=True) #
    okfs_code = models.CharField(max_length=50, blank=True, null=True) #
    okfs = models.CharField(max_length=500, blank=True, null=True) #
    is_active = models.CharField(max_length=10, blank=True, null=True)
    id_child = models.CharField(max_length=100, blank=True, null=True)
    individual = models.CharField(max_length=100, blank=True, null=True)

class Orgs(models.Model):
    id_company = models.IntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    inn = models.CharField(max_length=20, blank=True, null=True)
    yr_address = models.CharField(max_length=500, blank=True, null=True)
    real_address = models.CharField(max_length=500, blank=True, null=True)
    ogrn = models.CharField(max_length=20, blank=True, null=True)
    head_or_branch = models.PositiveSmallIntegerField(blank=True, null=True)
    kpp = models.CharField(max_length=50, blank=True, null=True) #???
    okopf_code = models.CharField(max_length=50, blank=True, null=True) #
    okopf = models.CharField(max_length=500, blank=True, null=True) #
    okvad2 = models.CharField(max_length=500, blank=True, null=True) #
    okvad2_full = models.CharField(max_length=2000, blank=True, null=True) #
    creation_time = models.CharField(max_length=23, blank=True, null=True) #
    egrul_status = models.CharField(max_length=500, blank=True, null=True) #
    okfs_code = models.CharField(max_length=50, blank=True, null=True) #
    okfs = models.CharField(max_length=500, blank=True, null=True) #
    is_active = models.CharField(max_length=10, blank=True, null=True)
    id_child = models.CharField(max_length=100, blank=True, null=True)
    tel_SPARK = models.CharField(max_length=50000, blank=True, null=True) #
    site = models.CharField(max_length=5000, blank=True, null=True) #
    principal = models.CharField(max_length=500, blank=True, null=True)
    position = models.CharField(max_length=1000, blank=True, null=True) #
    okvad2_add = models.CharField(max_length=25000, blank=True, null=True) #

class Files(models.Model):
    file = models.CharField(max_length=500)
    datetime = models.DateTimeField(auto_now_add=True)
    percent = models.PositiveSmallIntegerField()

class Reports(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    invention_bd = models.BooleanField(blank=False)
    pmodels_bd = models.BooleanField(blank=False)
    prom_bd = models.BooleanField(blank=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    inn = models.CharField(max_length=10000, blank=True, null=True)
    okopf = models.CharField(max_length=10000, blank=True, null=True)
    okopf_code = models.CharField(max_length=10000, blank=True, null=True)
    okfs = models.CharField(max_length=10000, blank=True, null=True)
    okfs_code = models.CharField(max_length=10000, blank=True, null=True)
    file = models.CharField(max_length=200, blank=True, null=True)