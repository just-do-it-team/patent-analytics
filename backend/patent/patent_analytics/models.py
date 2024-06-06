from django.db import models

class Orgs(models.Model):
    ID_company = models.IntegerField()
    full_name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=200)
    INN = models.BigIntegerField()
    Yr_address = models.CharField(max_length=200)
    real_address = models.CharField(max_length=200)
    OGRN = models.BigIntegerField()
    head_or_branch = models.PositiveSmallIntegerField()
    KPP = models.IntegerField()
    OKOPF_code = models.IntegerField()
    OKOPF = models.CharField(max_length=100)
    OKVAD2 = models.CharField(max_length=50)
    OKVAD2_full = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    EGRUL_status = models.CharField(max_length=20)
    OKFS_code = models.PositiveIntegerField()
    OKFS = models.CharField(max_length=50)
    is_active = models.PositiveSmallIntegerField()
    ID_child = models.CharField(max_length=100)
    tel_SPARK = models.CharField(max_length=5000)
    mail_SPARK = models.CharField(max_length=100)
    site = models.CharField(max_length=50)
    principal = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    OKVAD2_add = models.CharField(max_length=200)

class Pmbd(models.Model):
    reg_number = models.CharField(max_length=12) ######################
    reg_date = models.DateTimeField()
    application_number = models.PositiveBigIntegerField()
    application_date = models.DateTimeField()
    authors = models.CharField(max_length=3000)
    authors_latin = models.CharField(max_length=3000)
    patent_holders = models.CharField(max_length=1500)
    patent_holders_latin = models.CharField(max_length=700)
    correspondence_address = models.CharField(max_length=5500)
    correspondence_address_latin = models.CharField(max_length=1100)
    invention_name = models.CharField(max_length=1100)
    patent_starting_date = models.CharField(max_length=120)
    crimean_invention_application_number_for_state_registration_in_ukraine = models.CharField(max_length=60)
    crimean_invention_application_date_for_state_registration_in_ukraine = models.CharField(max_length=70)
    crimean_invention_patent_number_in_ukraine = models.PositiveBigIntegerField()
    receipt_date_of_additional_data_to_application = models.DateTimeField()  #дата поступления дополнительных данных к заявке
    date_of_application_to_wich_additional_data_has_been_received = models.DateTimeField()  #дата обращения, к которому получены дополнительные данные
    number_of_application_to_wich_additional_data_has_been_received = models.PositiveBigIntegerField()  #номер приложения, на которое были получены дополнительные данные
    initial_application_number = models.PositiveBigIntegerField()
    initial_application_date = models.DateTimeField()
    initial_application_priority_date = models.DateTimeField()  #дата приоритета?? первоначальной заявки
    previous_application_number = models.CharField(max_length=20)
    previous_application_date = models.DateTimeField()
    paris_convention_priority_number = models.CharField(max_length=1700)  #Приоритетный номер Парижской конвенции???
    paris_convention_priority_date = models.CharField(max_length=32)
    paris_convention_priority_country = models.CharField(max_length=350)
    pct_application_examination_start_date = models.DateTimeField()
    pct_application_number = models.CharField(max_length=20)
    pct_application_date = models.DateTimeField()
    pct_application_publish_number = models.PositiveBigIntegerField()
    pct_application_publish_date = models.DateTimeField()
    ea_application_number = models.PositiveIntegerField()
    ea_application_date = models.PositiveIntegerField()
    ea_application_publish_number = models.PositiveIntegerField()
    ea_application_publish_date = models.PositiveIntegerField()


