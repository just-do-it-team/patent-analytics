import json
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.http import FileResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from patent.settings import MEDIA_ROOT, BASE_DIR
from .models import Files, Reports, Invention_bd, Prom_bd, PModels_bd
from .serializer import FilesSerializer, ReportsSerializer
from .input_validation import validate_string, validate_list
from .bd_columns import prom_bd_excel, invention_bd_excel, pmodels_bd_excel
import zipfile
import datetime
import random
import os
import pandas as pd


class Pagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class Upload(APIView):
    def post(self, request):  # функция для загрузки нескольких файлов на сервер
        uploaded_files = request.FILES.getlist('files')
        processed_files = []
        processed_file_name = ''
        for file in uploaded_files:
            content = file.read()
            processed_content = content
            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
            processed_file_name = file.name.split('.')[0] + name_suffix + '.' + file.name.split('.')[1]
            processed_file_path = default_storage.save(processed_file_name, ContentFile(processed_content))
            processed_files.append(processed_file_path)
        ################################ запрос в базу по ИНН и другим полям
        df = pd.read_excel(os.path.join(BASE_DIR, 'xlsx/' + processed_file_name))
        inn_list = df['ИНН'].dropna()
        query = Invention_bd.objects.filter(inn__in=inn_list).values_list(
            'registration_number', 'registration_date', 'application_number',
            'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin',
            'correspondence_address', 'correspondence_address_latin', 'invention_name',
            'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date',
            'crimean_invention_patent_number_in_ukraine',
            'receipt_date_of_additional_data_to_application',
            'date_of_application_to_wich_additional_data_has_been_received',
            'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number',
            'initial_application_date',
            'initial_application_priority_date', 'previous_application_number', 'previous_application_date',
            'paris_convention_priority_number',
            'paris_convention_priority_date', 'paris_convention_priority_country',
            'pct_application_examination_start_date', 'pct_application_number',
            'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date',
            'ea_application_number',
            'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date',
            'application_publish_date',
            'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number',
            'revoke_patent_number',
            'information_about_the_obligation', 'expiration_date',
            'invention_formula_numbers_for_which_patent_term_is_prolonged',
            'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch',
            'id_child', 'inn', 'is_active',
            'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
        query2 = PModels_bd.objects.filter(inn__in=inn_list).values_list(
            'registration_number',
            'registration_date',
            'application_number',
            'application_date', 'authors',
            'authors_latin', 'patent_holders',
            'patent_holders_latin',
            'correspondence_address',
            'correspondence_address_latin',
            'utility_model_name',
            'patent_starting_date',
            'crimean_utility_application_number',
            'crimean_utility_application_date',
            'crimean_utility_patent_number_in_ukraine',
            'receipt_date_of_additional_data_to_application',
            'date_of_application_to_wich_additional_data_has_been_received',
            'number_of_application_to_wich_additional_data_has_been_received',
            'initial_application_number',
            'initial_application_date',
            'initial_application_priority_date',
            'previous_application_number',
            'previous_application_date',
            'paris_convention_priority_number',
            'paris_convention_priority_date',
            'paris_convention_priority_country',
            'pct_application_examination_start_date',
            'pct_application_number',
            'pct_application_date',
            'pct_application_publish_number',
            'pct_application_publish_date',
            'patent_grant_publish_date',
            'patent_grant_publish_number',
            'revoke_patent_number',
            'expiration_date',
            'utility_formula_numbers_for_which_patent_term_is_prolonged',
            'actual', 'publication_url', 'mpk',
            'unnamed_39', 'unnamed_40',
            'head_or_branch', 'id_child', 'inn',
            'is_active', 'ogrn',
            'okopf', 'okopf_code', 'okfs',
            'okfs_code')
        query3 = Prom_bd.objects.filter(inn__in=inn_list).values_list(
            'registration_number', 'registration_date', 'application_number', 'application_date', 'authors',
            'authors_latin', 'patent_holders',
            'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name',
            'patent_starting_date',
            'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
            'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
            'date_of_application_to_wich_additional_data_has_been_received',
            'number_of_application_to_wich_additional_data_has_been_received',
            'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
            'previous_application_number', 'previous_application_date',
            'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
            'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
            'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
            'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active',
            'ogrn',
            'okopf', 'okopf_code', 'okfs', 'okfs_code')
        df = pd.DataFrame(list(query), columns=invention_bd_excel())
        df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
        df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
        df = pd.concat([df, df2, df3])
        df['registration date'] = pd.to_datetime(df['registration date'])
        df['expiration date'] = pd.to_datetime(df['expiration date'])
        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
        processed_file_name = f'{name_suffix}.xlsx'
        path_to_file = os.path.join(BASE_DIR, 'xlsx/' + processed_file_name)
        found_inn = df['inn'].nunique()
        percent = round(len(inn_list)/ (found_inn+1))
        df.to_excel(path_to_file)
        Files.objects.create(file=processed_file_name, percent=percent)
        return Response({"processed_files": f'{processed_file_name}'}, status=status.HTTP_200_OK)


    #функция для скачивания файла с сервера (например file_path = 'xlsx/text.txt') папка см комментарий к MEDIA_ROOT
    def get(self, request):
        filename = Files.objects.order_by("-id").values('file')[0]
        file_path = os.path.join(BASE_DIR, 'xlsx/' + filename['file'])
        # file_path = 'xlsx/' + filename['file']
        response = FileResponse(open(file_path, 'rb'))
        return response


class File_history_get_file(APIView):
    def post(self,request):
        body = json.loads(request.body.decode('utf-8'))
        ids = body.get('ids')
        if len(ids) == 1:
            filename = Files.objects.filter(id__in=ids).values('id', 'file')[0]
            file_path = os.path.join(BASE_DIR, 'xlsx/' + filename['file'])
            # file_path = 'xlsx/' + filename['file']
            response = FileResponse(open(file_path, 'rb'))
            return response
        elif len(ids) > 1:
            filenames = Files.objects.filter(id__in=ids).values('id', 'file')
            file_list = []
            for file in filenames:
                file_list.append(pd.read_excel(str(os.path.join(BASE_DIR, 'xlsx/' + file['file']))))
            endfile = pd.concat(file_list, ignore_index=True)
            endfile = endfile.drop_duplicates(subset=['registration number'])
            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0,100))
            filename = f'{MEDIA_ROOT}{name_suffix}.xlsx'
            endfile.to_excel(filename)
            response = FileResponse(open(filename, 'rb'))
            return response

class File_history(ListAPIView):
    pagination_class = Pagination
    serializer_class = FilesSerializer
    def get_queryset(self):
        return Files.objects.order_by("-id")

class Report_history(ListAPIView):
    pagination_class = Pagination
    serializer_class = ReportsSerializer
    def get_queryset(self):
        return Reports.objects.order_by("-id")

class Filter_history_view(APIView):
    def get(self, request):
        report_id = self.request.query_params.get('id', None)
        if report_id is not None:
            reports_query = Reports.objects.get(id=report_id)
            serializer = ReportsSerializer(reports_query)
            return Response(serializer.data)

class Report(APIView):
    def post(self,request):
        body = json.loads(request.body.decode('utf-8'))
        invention_bd, pmodels_bd, prom_bd = body.get('invention_bd'), body.get('pmodels_bd'), body.get('prom_bd')
        start_date = body.get('start_date')
        if start_date is None:
            start_date = '{:%Y-%m-%d}'.format(datetime.datetime.today() - datetime.timedelta(days=365))
        end_date = body.get('end_date')
        if end_date is None:
            end_date = '{:%Y-%m-%d}'.format(datetime.datetime.today())
        inn, okopf, okopf_code = body.get('inn'), body.get('okopf'), body.get('okopf_code')
        # okfs, okfs_code = body.get('okfs'), body.get('okfs_code')
############ 1)
        if invention_bd and not pmodels_bd and not prom_bd:
            if inn is not None: #1
                if validate_string(inn):
                    if okopf is not None: #2
                        if validate_list(okopf):
                            if okopf_code is not None: #3
                                if validate_list(okopf_code):
                                    query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                    df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                            else: #4
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number','registration_date', 'application_number',
                                          'application_date', 'authors','authors_latin', 'patent_holders', 'patent_holders_latin',
                                          'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                          'patent_starting_date', 'crimean_invention_application_number',
                                          'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                          'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                          'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number',
                                          'initial_application_date', 'initial_application_priority_date',
                                          'previous_application_number',  'previous_application_date', 'paris_convention_priority_number',
                                          'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date',
                                          'pct_application_number', 'pct_application_date', 'pct_application_publish_number',
                                          'pct_application_publish_date', 'ea_application_number', 'ea_application_date',
                                          'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                          'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number',
                                          'revoke_patent_number', 'information_about_the_obligation', 'expiration_date',
                                          'invention_formula_numbers_for_which_patent_term_is_prolonged', 'additional_patent', 'actual', 'mpk',
                                          'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                          'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                    else: #5
                        if okopf_code is not None: #6
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number',
                                           'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                           'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                           'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                           'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                           'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                           'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                           'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                           'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                           'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                           'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                           'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                            'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else: #7
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number','registration_date', 'application_number',
                                      'application_date', 'authors','authors_latin', 'patent_holders', 'patent_holders_latin',
                                      'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                      'patent_starting_date', 'crimean_invention_application_number',
                                      'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number',
                                      'initial_application_date', 'initial_application_priority_date',
                                      'previous_application_number',  'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date',
                                      'pct_application_number', 'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'ea_application_number', 'ea_application_date',
                                      'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                      'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number',
                                      'revoke_patent_number', 'information_about_the_obligation', 'expiration_date',
                                      'invention_formula_numbers_for_which_patent_term_is_prolonged', 'additional_patent', 'actual', 'mpk',
                                      'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                      'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    JsonResponse({"error": "Ошибка в поле ИНН"},status=400)
            else: #8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number',
                                                                                  'registration_date',
                                                                                  'application_number',
                                                                                  'application_date', 'authors',
                                                                                  'authors_latin', 'patent_holders',
                                                                                  'patent_holders_latin',
                                                                                  'correspondence_address',
                                                                                  'correspondence_address_latin',
                                                                                  'invention_name',
                                                                                  'patent_starting_date',
                                                                                  'crimean_invention_application_number',
                                                                                  'crimean_invention_application_date',
                                                                                  'crimean_invention_patent_number_in_ukraine',
                                                                                  'receipt_date_of_additional_data_to_application',
                                                                                  'date_of_application_to_wich_additional_data_has_been_received',
                                                                                  'number_of_application_to_wich_additional_data_has_been_received',
                                                                                  'initial_application_number',
                                                                                  'initial_application_date',
                                                                                  'initial_application_priority_date',
                                                                                  'previous_application_number',
                                                                                  'previous_application_date',
                                                                                  'paris_convention_priority_number',
                                                                                  'paris_convention_priority_date',
                                                                                  'paris_convention_priority_country',
                                                                                  'pct_application_examination_start_date',
                                                                                  'pct_application_number',
                                                                                  'pct_application_date',
                                                                                  'pct_application_publish_number',
                                                                                  'pct_application_publish_date',
                                                                                  'ea_application_number',
                                                                                  'ea_application_date',
                                                                                  'ea_application_publish_number',
                                                                                  'ea_application_publish_date',
                                                                                  'application_publish_date',
                                                                                  'application_publish_number',
                                                                                  'patent_grant_publish_date',
                                                                                  'patent_grant_publish_number',
                                                                                  'revoke_patent_number',
                                                                                  'information_about_the_obligation',
                                                                                  'expiration_date',
                                                                                  'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                                                                  'additional_patent', 'actual',
                                                                                  'mpk', 'unnamed_46', 'unnamed_47',
                                                                                  'unnamed_48', 'head_or_branch',
                                                                                  'id_child', 'inn', 'is_active',
                                                                                  'ogrn', 'okfs', 'okfs_code',
                                                                                  'okopf', 'okopf_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 11
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list(
                                'registration_number', 'registration_date', 'application_number',
                                'application_date', 'authors', 'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                'patent_starting_date', 'crimean_invention_application_number',
                                'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date', 'initial_application_priority_date',
                                'previous_application_number', 'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date', 'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number', 'pct_application_date', 'pct_application_publish_number',
                                'pct_application_publish_date', 'ea_application_number', 'ea_application_date',
                                'ea_application_publish_number', 'ea_application_publish_date',
                                'application_publish_date',
                                'application_publish_number', 'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number', 'information_about_the_obligation', 'expiration_date',
                                'invention_formula_numbers_for_which_patent_term_is_prolonged', 'additional_patent',
                                'actual', 'mpk',
                                'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn',
                                'is_active',
                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number',
                                                  'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                                  'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                                  'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date',
                                                  'crimean_invention_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                                  'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                                  'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                                  'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                                  'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date',
                                                  'pct_application_number', 'pct_application_date', 'pct_application_publish_number',
                                                  'pct_application_publish_date', 'ea_application_number', 'ea_application_date', 'ea_application_publish_number',
                                                  'ea_application_publish_date', 'application_publish_date',
                                                  'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                                  'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                                  'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch',
                                                  'id_child', 'inn', 'is_active', 'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                    else:  # 14
                        query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list(
                            'registration_number', 'registration_date', 'application_number',
                            'application_date', 'authors', 'authors_latin', 'patent_holders',
                            'patent_holders_latin',
                            'correspondence_address', 'correspondence_address_latin', 'invention_name',
                            'patent_starting_date', 'crimean_invention_application_number',
                            'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                            'receipt_date_of_additional_data_to_application',
                            'date_of_application_to_wich_additional_data_has_been_received',
                            'number_of_application_to_wich_additional_data_has_been_received',
                            'initial_application_number',
                            'initial_application_date', 'initial_application_priority_date',
                            'previous_application_number', 'previous_application_date',
                            'paris_convention_priority_number',
                            'paris_convention_priority_date', 'paris_convention_priority_country',
                            'pct_application_examination_start_date',
                            'pct_application_number', 'pct_application_date', 'pct_application_publish_number',
                            'pct_application_publish_date', 'ea_application_number', 'ea_application_date',
                            'ea_application_publish_number', 'ea_application_publish_date',
                            'application_publish_date',
                            'application_publish_number', 'patent_grant_publish_date',
                            'patent_grant_publish_number',
                            'revoke_patent_number', 'information_about_the_obligation', 'expiration_date',
                            'invention_formula_numbers_for_which_patent_term_is_prolonged', 'additional_patent',
                            'actual', 'mpk',
                            'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn',
                            'is_active',
                            'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                        df = pd.DataFrame(list(query), columns=invention_bd_excel())
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))
############################ 2)
        elif not invention_bd and pmodels_bd and not prom_bd:
            if inn is not None:  # 1
                if validate_string(inn):
                    if okopf is not None:  # 2
                        if validate_list(okopf):
                            if okopf_code is not None:  # 3
                                if validate_list(okopf_code):
                                    query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in
                                                                                   okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in
                                                                                        okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                    df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                            else:  # 4
                                query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in
                                                                               okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                    else:  # 5
                        if okopf_code is not None:  # 6
                            if validate_list(okopf_code):
                                query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in
                                                                                    okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 7
                            query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in
                                                                         inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    return JsonResponse({"error": "Ошибка в поле ИНН"},status=400)
            else:  # 8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in
                                                                               okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in
                                                                                    okopf_code.split(
                                                                                        ';')]).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 11
                            query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in
                                                                                okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                    else:  # 14
                        query = PModels_bd.objects.filter(
                            registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number',
                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                      'patent_holders_latin', 'correspondence_address',
                                      'correspondence_address_latin', 'utility_model_name',
                                      'patent_starting_date',
                                      'crimean_utility_application_number',
                                      'crimean_utility_application_date',
                                      'crimean_utility_patent_number_in_ukraine',
                                      'receipt_date_of_additional_data_to_application',
                                      'date_of_application_to_wich_additional_data_has_been_received',
                                      'number_of_application_to_wich_additional_data_has_been_received',
                                      'initial_application_number', 'initial_application_date',
                                      'initial_application_priority_date', 'previous_application_number',
                                      'previous_application_date', 'paris_convention_priority_number',
                                      'paris_convention_priority_date',
                                      'paris_convention_priority_country',
                                      'pct_application_examination_start_date', 'pct_application_number',
                                      'pct_application_date', 'pct_application_publish_number',
                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                      'patent_grant_publish_number', 'revoke_patent_number',
                                      'expiration_date',
                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs', 'okfs_code')
                        df = pd.DataFrame(list(query), columns=pmodels_bd_excel())
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))
############################ 3)
        elif not invention_bd and not pmodels_bd and prom_bd:
            if inn is not None:  # 1
                if validate_string(inn):
                    if okopf is not None:  # 2
                        if validate_list(okopf):
                            if okopf_code is not None:  # 3
                                if validate_list(okopf_code):
                                    query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in
                                                                                   okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in
                                                                                        okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                    df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                        random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                            else:  # 4
                                query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in
                                                                               okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                    else:  # 5
                        if okopf_code is not None:  # 6
                            if validate_list(okopf_code):
                                query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in
                                                                                    okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 7
                            query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in
                                                                         inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=prom_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    return JsonResponse({"error": "Ошибка в поле ИНН"},status=400)
            else:  # 8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in
                                                                               okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in
                                                                                    okopf_code.split(
                                                                                        ';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 11
                            query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=prom_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in
                                                                                okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=prom_bd_excel())
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                    else:  # 14
                        query = Prom_bd.objects.filter(
                            registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                        df = pd.DataFrame(list(query), columns=prom_bd_excel())
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))
############################ 4)
        elif invention_bd and pmodels_bd and not prom_bd:
            if inn is not None: #1
                if validate_string(inn):
                    if okopf is not None: #2
                        if validate_list(okopf):
                            if okopf_code is not None: #3
                                if validate_list(okopf_code):
                                    query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                    query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                      inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                      okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                      okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number',
                                                                                    'registration_date',
                                                                                    'application_number',
                                                                                    'application_date', 'authors',
                                                                                    'authors_latin', 'patent_holders',
                                                                                    'patent_holders_latin',
                                                                                    'correspondence_address',
                                                                                    'correspondence_address_latin',
                                                                                    'utility_model_name',
                                                                                    'patent_starting_date',
                                                                                    'crimean_utility_application_number',
                                                                                    'crimean_utility_application_date',
                                                                                    'crimean_utility_patent_number_in_ukraine',
                                                                                    'receipt_date_of_additional_data_to_application',
                                                                                    'date_of_application_to_wich_additional_data_has_been_received',
                                                                                    'number_of_application_to_wich_additional_data_has_been_received',
                                                                                    'initial_application_number',
                                                                                    'initial_application_date',
                                                                                    'initial_application_priority_date',
                                                                                    'previous_application_number',
                                                                                    'previous_application_date',
                                                                                    'paris_convention_priority_number',
                                                                                    'paris_convention_priority_date',
                                                                                    'paris_convention_priority_country',
                                                                                    'pct_application_examination_start_date',
                                                                                    'pct_application_number',
                                                                                    'pct_application_date',
                                                                                    'pct_application_publish_number',
                                                                                    'pct_application_publish_date',
                                                                                    'patent_grant_publish_date',
                                                                                    'patent_grant_publish_number',
                                                                                    'revoke_patent_number',
                                                                                    'expiration_date',
                                                                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                                                                    'actual', 'publication_url', 'mpk',
                                                                                    'unnamed_39', 'unnamed_40',
                                                                                    'head_or_branch', 'id_child', 'inn',
                                                                                    'is_active', 'ogrn',
                                                                                    'okopf', 'okopf_code', 'okfs',
                                                                                    'okfs_code')
                                    df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                    df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                    df = pd.concat([df, df2])
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                            else: #4
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                    else: #5
                        if okopf_code is not None: #6
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else: #7
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               inn__in=[x.strip(' ') for x in inn.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    JsonResponse({"error": "Ошибка в поле ИНН"},status=400)
            else: #8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in
                                                                                   okopf_code.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 11
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf_code__in=[y.strip(' ') for y in
                                                                               okopf_code.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                    else:  # 14
                        query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                        query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list(
                            'registration_number',
                            'registration_date',
                            'application_number',
                            'application_date', 'authors',
                            'authors_latin', 'patent_holders',
                            'patent_holders_latin',
                            'correspondence_address',
                            'correspondence_address_latin',
                            'utility_model_name',
                            'patent_starting_date',
                            'crimean_utility_application_number',
                            'crimean_utility_application_date',
                            'crimean_utility_patent_number_in_ukraine',
                            'receipt_date_of_additional_data_to_application',
                            'date_of_application_to_wich_additional_data_has_been_received',
                            'number_of_application_to_wich_additional_data_has_been_received',
                            'initial_application_number',
                            'initial_application_date',
                            'initial_application_priority_date',
                            'previous_application_number',
                            'previous_application_date',
                            'paris_convention_priority_number',
                            'paris_convention_priority_date',
                            'paris_convention_priority_country',
                            'pct_application_examination_start_date',
                            'pct_application_number',
                            'pct_application_date',
                            'pct_application_publish_number',
                            'pct_application_publish_date',
                            'patent_grant_publish_date',
                            'patent_grant_publish_number',
                            'revoke_patent_number',
                            'expiration_date',
                            'utility_formula_numbers_for_which_patent_term_is_prolonged',
                            'actual', 'publication_url', 'mpk',
                            'unnamed_39', 'unnamed_40',
                            'head_or_branch', 'id_child', 'inn',
                            'is_active', 'ogrn',
                            'okopf', 'okopf_code', 'okfs',
                            'okfs_code')
                        df = pd.DataFrame(list(query), columns=invention_bd_excel())
                        df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                        df = pd.concat([df,df2])
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))
############################ 5)
        elif not invention_bd and pmodels_bd and prom_bd:
            if inn is not None:  # 1
                if validate_string(inn):
                    if okopf is not None:  # 2
                        if validate_list(okopf):
                            if okopf_code is not None:  # 3
                                if validate_list(okopf_code):
                                    query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                    query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                       inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                       okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                       okopf_code__in=[y.strip(' ') for y in
                                                                                       okopf_code.split(';')]).values_list(
                                        'registration_number',
                                        'registration_date',
                                        'application_number',
                                        'application_date', 'authors',
                                        'authors_latin', 'patent_holders',
                                        'patent_holders_latin',
                                        'correspondence_address',
                                        'correspondence_address_latin',
                                        'utility_model_name',
                                        'patent_starting_date',
                                        'crimean_utility_application_number',
                                        'crimean_utility_application_date',
                                        'crimean_utility_patent_number_in_ukraine',
                                        'receipt_date_of_additional_data_to_application',
                                        'date_of_application_to_wich_additional_data_has_been_received',
                                        'number_of_application_to_wich_additional_data_has_been_received',
                                        'initial_application_number',
                                        'initial_application_date',
                                        'initial_application_priority_date',
                                        'previous_application_number',
                                        'previous_application_date',
                                        'paris_convention_priority_number',
                                        'paris_convention_priority_date',
                                        'paris_convention_priority_country',
                                        'pct_application_examination_start_date',
                                        'pct_application_number',
                                        'pct_application_date',
                                        'pct_application_publish_number',
                                        'pct_application_publish_date',
                                        'patent_grant_publish_date',
                                        'patent_grant_publish_number',
                                        'revoke_patent_number',
                                        'expiration_date',
                                        'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                        'actual', 'publication_url', 'mpk',
                                        'unnamed_39', 'unnamed_40',
                                        'head_or_branch', 'id_child', 'inn',
                                        'is_active', 'ogrn',
                                        'okopf', 'okopf_code', 'okfs',
                                        'okfs_code')
                                    df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                    df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                    df = pd.concat([df, df2])
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"}, status=400)
                            else:  # 4
                                query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"}, status=400)
                    else:  # 5
                        if okopf_code is not None:  # 6
                            if validate_list(okopf_code):
                                query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in
                                                                                   okopf_code.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"}, status=400)
                        else:  # 7
                            query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               inn__in=[x.strip(' ') for x in inn.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            df = pd.DataFrame(list(query), columns=prom_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    JsonResponse({"error": "Ошибка в поле ИНН"}, status=400)
            else:  # 8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in
                                                                                    okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in
                                                                                   okopf_code.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                df = pd.DataFrame(list(query), columns=prom_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"}, status=400)
                        else:  # 11
                            query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            df = pd.DataFrame(list(query), columns=prom_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"}, status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in
                                                                                okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf_code__in=[y.strip(' ') for y in
                                                                               okopf_code.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            df = pd.DataFrame(list(query), columns=prom_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"}, status=400)
                    else:  # 14
                        query = Prom_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                        query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list(
                            'registration_number',
                            'registration_date',
                            'application_number',
                            'application_date', 'authors',
                            'authors_latin', 'patent_holders',
                            'patent_holders_latin',
                            'correspondence_address',
                            'correspondence_address_latin',
                            'utility_model_name',
                            'patent_starting_date',
                            'crimean_utility_application_number',
                            'crimean_utility_application_date',
                            'crimean_utility_patent_number_in_ukraine',
                            'receipt_date_of_additional_data_to_application',
                            'date_of_application_to_wich_additional_data_has_been_received',
                            'number_of_application_to_wich_additional_data_has_been_received',
                            'initial_application_number',
                            'initial_application_date',
                            'initial_application_priority_date',
                            'previous_application_number',
                            'previous_application_date',
                            'paris_convention_priority_number',
                            'paris_convention_priority_date',
                            'paris_convention_priority_country',
                            'pct_application_examination_start_date',
                            'pct_application_number',
                            'pct_application_date',
                            'pct_application_publish_number',
                            'pct_application_publish_date',
                            'patent_grant_publish_date',
                            'patent_grant_publish_number',
                            'revoke_patent_number',
                            'expiration_date',
                            'utility_formula_numbers_for_which_patent_term_is_prolonged',
                            'actual', 'publication_url', 'mpk',
                            'unnamed_39', 'unnamed_40',
                            'head_or_branch', 'id_child', 'inn',
                            'is_active', 'ogrn',
                            'okopf', 'okopf_code', 'okfs',
                            'okfs_code')
                        df = pd.DataFrame(list(query), columns=prom_bd_excel())
                        df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                        df = pd.concat([df, df2])
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))
############################ 6)
        elif invention_bd and not pmodels_bd and prom_bd:
            if inn is not None: #1
                if validate_string(inn):
                    if okopf is not None: #2
                        if validate_list(okopf):
                            if okopf_code is not None: #3
                                if validate_list(okopf_code):
                                    query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                    query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                      inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                      okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                      okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                    df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                    df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                                    df = pd.concat([df, df2])
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                            else: #4
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                    else: #5
                        if okopf_code is not None: #6
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else: #7
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    JsonResponse({"error": "Ошибка в поле ИНН"},status=400)
            else: #8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in
                                                                                   okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                                df = pd.concat([df, df2])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 11
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf_code__in=[y.strip(' ') for y in
                                                                               okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                            df = pd.concat([df, df2])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                    else:  # 14
                        query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                        query2 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                        df = pd.DataFrame(list(query), columns=invention_bd_excel())
                        df2 = pd.DataFrame(list(query2), columns=prom_bd_excel())
                        df = pd.concat([df,df2])
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))
######################### 7)
        elif invention_bd and pmodels_bd and prom_bd:
            if inn is not None: #1
                if validate_string(inn):
                    if okopf is not None: #2
                        if validate_list(okopf):
                            if okopf_code is not None: #3
                                if validate_list(okopf_code):
                                    query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                        inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                        okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                        okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                        ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                    query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                      inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                      okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                      okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number',
                                                                                    'registration_date',
                                                                                    'application_number',
                                                                                    'application_date', 'authors',
                                                                                    'authors_latin', 'patent_holders',
                                                                                    'patent_holders_latin',
                                                                                    'correspondence_address',
                                                                                    'correspondence_address_latin',
                                                                                    'utility_model_name',
                                                                                    'patent_starting_date',
                                                                                    'crimean_utility_application_number',
                                                                                    'crimean_utility_application_date',
                                                                                    'crimean_utility_patent_number_in_ukraine',
                                                                                    'receipt_date_of_additional_data_to_application',
                                                                                    'date_of_application_to_wich_additional_data_has_been_received',
                                                                                    'number_of_application_to_wich_additional_data_has_been_received',
                                                                                    'initial_application_number',
                                                                                    'initial_application_date',
                                                                                    'initial_application_priority_date',
                                                                                    'previous_application_number',
                                                                                    'previous_application_date',
                                                                                    'paris_convention_priority_number',
                                                                                    'paris_convention_priority_date',
                                                                                    'paris_convention_priority_country',
                                                                                    'pct_application_examination_start_date',
                                                                                    'pct_application_number',
                                                                                    'pct_application_date',
                                                                                    'pct_application_publish_number',
                                                                                    'pct_application_publish_date',
                                                                                    'patent_grant_publish_date',
                                                                                    'patent_grant_publish_number',
                                                                                    'revoke_patent_number',
                                                                                    'expiration_date',
                                                                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                                                                    'actual', 'publication_url', 'mpk',
                                                                                    'unnamed_39', 'unnamed_40',
                                                                                    'head_or_branch', 'id_child', 'inn',
                                                                                    'is_active', 'ogrn',
                                                                                    'okopf', 'okopf_code', 'okfs',
                                                                                    'okfs_code')
                                    query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in
                                                                                    okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                    df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                    df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                    df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                                    df = pd.concat([df, df2, df3])
                                    df['registration date'] = pd.to_datetime(df['registration date'])
                                    df['expiration date'] = pd.to_datetime(df['expiration date'])
                                    df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                    df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                    name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                    filename = f'{name_suffix}.xlsx'
                                    path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                    Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                           prom_bd=prom_bd,
                                                           start_date=start_date, end_date=end_date, inn=inn,
                                                           okopf=okopf,
                                                           okopf_code=okopf_code, file=filename)
                                    df.to_excel(path_to_file)
                                    return FileResponse(open(path_to_file, 'rb'))
                                else:
                                    return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                            else: #4
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                                df = pd.concat([df, df2, df3])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                    else: #5
                        if okopf_code is not None: #6
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]
                                                                    ).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')],
                                                                okopf_code__in=[y.strip(' ') for y in
                                                                                okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                                df = pd.concat([df, df2, df3])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else: #7
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               inn__in=[x.strip(' ') for x in inn.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                            inn__in=[x.strip(' ') for x in inn.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                            df = pd.concat([df, df2, df3])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                else:
                    JsonResponse({"error": "Ошибка в поле ИНН"},status=400)
            else: #8
                if okopf is not None:  # 9
                    if validate_list(okopf):
                        if okopf_code is not None:  # 10
                            if validate_list(okopf_code):
                                query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                    okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                    okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                                query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                   okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                   okopf_code__in=[y.strip(' ') for y in
                                                                                   okopf_code.split(';')]).values_list(
                                    'registration_number',
                                    'registration_date',
                                    'application_number',
                                    'application_date', 'authors',
                                    'authors_latin', 'patent_holders',
                                    'patent_holders_latin',
                                    'correspondence_address',
                                    'correspondence_address_latin',
                                    'utility_model_name',
                                    'patent_starting_date',
                                    'crimean_utility_application_number',
                                    'crimean_utility_application_date',
                                    'crimean_utility_patent_number_in_ukraine',
                                    'receipt_date_of_additional_data_to_application',
                                    'date_of_application_to_wich_additional_data_has_been_received',
                                    'number_of_application_to_wich_additional_data_has_been_received',
                                    'initial_application_number',
                                    'initial_application_date',
                                    'initial_application_priority_date',
                                    'previous_application_number',
                                    'previous_application_date',
                                    'paris_convention_priority_number',
                                    'paris_convention_priority_date',
                                    'paris_convention_priority_country',
                                    'pct_application_examination_start_date',
                                    'pct_application_number',
                                    'pct_application_date',
                                    'pct_application_publish_number',
                                    'pct_application_publish_date',
                                    'patent_grant_publish_date',
                                    'patent_grant_publish_number',
                                    'revoke_patent_number',
                                    'expiration_date',
                                    'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                    'actual', 'publication_url', 'mpk',
                                    'unnamed_39', 'unnamed_40',
                                    'head_or_branch', 'id_child', 'inn',
                                    'is_active', 'ogrn',
                                    'okopf', 'okopf_code', 'okfs',
                                    'okfs_code')
                                query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in okopf.split(';')],
                                                                okopf_code__in=[y.strip(' ') for y in
                                                                                okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                                df = pd.DataFrame(list(query), columns=invention_bd_excel())
                                df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                                df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                                df = pd.concat([df, df2, df3])
                                df['registration date'] = pd.to_datetime(df['registration date'])
                                df['expiration date'] = pd.to_datetime(df['expiration date'])
                                df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                                df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                                name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                    random.randint(0, 100))
                                filename = f'{name_suffix}.xlsx'
                                path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                                Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                       prom_bd=prom_bd,
                                                       start_date=start_date, end_date=end_date, inn=inn,
                                                       okopf=okopf,
                                                       okopf_code=okopf_code, file=filename)
                                df.to_excel(path_to_file)
                                return FileResponse(open(path_to_file, 'rb'))
                            else:
                                return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                        else:  # 11
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf__in=[y.strip(' ') for y in
                                                                           okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                            okopf__in=[y.strip(' ') for y in okopf.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                            df = pd.concat([df, df2, df3])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                    else:
                        return JsonResponse({"error": "Ошибка в поле ОКОПФ"},status=400)
                else:  # 12
                    if okopf_code is not None:  # 13
                        if validate_list(okopf_code):
                            query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                                okopf_code__in=[y.strip(' ') for y in okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                            query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                               okopf_code__in=[y.strip(' ') for y in
                                                                               okopf_code.split(';')]).values_list(
                                'registration_number',
                                'registration_date',
                                'application_number',
                                'application_date', 'authors',
                                'authors_latin', 'patent_holders',
                                'patent_holders_latin',
                                'correspondence_address',
                                'correspondence_address_latin',
                                'utility_model_name',
                                'patent_starting_date',
                                'crimean_utility_application_number',
                                'crimean_utility_application_date',
                                'crimean_utility_patent_number_in_ukraine',
                                'receipt_date_of_additional_data_to_application',
                                'date_of_application_to_wich_additional_data_has_been_received',
                                'number_of_application_to_wich_additional_data_has_been_received',
                                'initial_application_number',
                                'initial_application_date',
                                'initial_application_priority_date',
                                'previous_application_number',
                                'previous_application_date',
                                'paris_convention_priority_number',
                                'paris_convention_priority_date',
                                'paris_convention_priority_country',
                                'pct_application_examination_start_date',
                                'pct_application_number',
                                'pct_application_date',
                                'pct_application_publish_number',
                                'pct_application_publish_date',
                                'patent_grant_publish_date',
                                'patent_grant_publish_number',
                                'revoke_patent_number',
                                'expiration_date',
                                'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                'actual', 'publication_url', 'mpk',
                                'unnamed_39', 'unnamed_40',
                                'head_or_branch', 'id_child', 'inn',
                                'is_active', 'ogrn',
                                'okopf', 'okopf_code', 'okfs',
                                'okfs_code')
                            query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date],
                                                            okopf_code__in=[y.strip(' ') for y in
                                                                            okopf_code.split(';')]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                            df = pd.DataFrame(list(query), columns=invention_bd_excel())
                            df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                            df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                            df = pd.concat([df, df2, df3])
                            df['registration date'] = pd.to_datetime(df['registration date'])
                            df['expiration date'] = pd.to_datetime(df['expiration date'])
                            df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                            df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                            name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(
                                random.randint(0, 100))
                            filename = f'{name_suffix}.xlsx'
                            path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                            Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                                   prom_bd=prom_bd,
                                                   start_date=start_date, end_date=end_date, inn=inn,
                                                   okopf=okopf,
                                                   okopf_code=okopf_code, file=filename)
                            df.to_excel(path_to_file)
                            return FileResponse(open(path_to_file, 'rb'))
                        else:
                            return JsonResponse({"error": "Ошибка в поле ОКОПФ коды"},status=400)
                    else:  # 14
                        query = Invention_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number',
                                               'application_date', 'authors', 'authors_latin', 'patent_holders', 'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'invention_name',
                                               'patent_starting_date', 'crimean_invention_application_number', 'crimean_invention_application_date', 'crimean_invention_patent_number_in_ukraine',
                                               'receipt_date_of_additional_data_to_application', 'date_of_application_to_wich_additional_data_has_been_received',
                                               'number_of_application_to_wich_additional_data_has_been_received', 'initial_application_number', 'initial_application_date',
                                               'initial_application_priority_date', 'previous_application_number', 'previous_application_date', 'paris_convention_priority_number',
                                               'paris_convention_priority_date', 'paris_convention_priority_country', 'pct_application_examination_start_date', 'pct_application_number',
                                               'pct_application_date', 'pct_application_publish_number', 'pct_application_publish_date', 'ea_application_number',
                                               'ea_application_date', 'ea_application_publish_number', 'ea_application_publish_date', 'application_publish_date',
                                               'application_publish_number', 'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                               'information_about_the_obligation', 'expiration_date', 'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                               'additional_patent', 'actual', 'mpk', 'unnamed_46', 'unnamed_47', 'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
                        query2 = PModels_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list(
                            'registration_number',
                            'registration_date',
                            'application_number',
                            'application_date', 'authors',
                            'authors_latin', 'patent_holders',
                            'patent_holders_latin',
                            'correspondence_address',
                            'correspondence_address_latin',
                            'utility_model_name',
                            'patent_starting_date',
                            'crimean_utility_application_number',
                            'crimean_utility_application_date',
                            'crimean_utility_patent_number_in_ukraine',
                            'receipt_date_of_additional_data_to_application',
                            'date_of_application_to_wich_additional_data_has_been_received',
                            'number_of_application_to_wich_additional_data_has_been_received',
                            'initial_application_number',
                            'initial_application_date',
                            'initial_application_priority_date',
                            'previous_application_number',
                            'previous_application_date',
                            'paris_convention_priority_number',
                            'paris_convention_priority_date',
                            'paris_convention_priority_country',
                            'pct_application_examination_start_date',
                            'pct_application_number',
                            'pct_application_date',
                            'pct_application_publish_number',
                            'pct_application_publish_date',
                            'patent_grant_publish_date',
                            'patent_grant_publish_number',
                            'revoke_patent_number',
                            'expiration_date',
                            'utility_formula_numbers_for_which_patent_term_is_prolonged',
                            'actual', 'publication_url', 'mpk',
                            'unnamed_39', 'unnamed_40',
                            'head_or_branch', 'id_child', 'inn',
                            'is_active', 'ogrn',
                            'okopf', 'okopf_code', 'okfs',
                            'okfs_code')
                        query3 = Prom_bd.objects.filter(registration_date__range=[start_date, end_date]).values_list('registration_number', 'registration_date', 'application_number', 'application_date', 'authors', 'authors_latin', 'patent_holders',
                                             'patent_holders_latin', 'correspondence_address', 'correspondence_address_latin', 'industrial_design_name', 'patent_starting_date',
                                             'crimean_industrial_design_application_number', 'crimean_industrial_design_application_date',
                                             'crimean_industrial_design_patent_number_in_ukraine', 'receipt_date_of_additional_data_to_application',
                                             'date_of_application_to_wich_additional_data_has_been_received', 'number_of_application_to_wich_additional_data_has_been_received',
                                             'initial_application_number', 'initial_application_date', 'initial_application_priority_date',
                                             'previous_application_number', 'previous_application_date',
                                             'paris_convention_priority_number', 'paris_convention_priority_date', 'paris_convention_priority_country',
                                             'patent_grant_publish_date', 'patent_grant_publish_number', 'revoke_patent_number',
                                             'expiration_date', 'numbers_of_list_of_essential_features', 'industrial_designs_names_and_number',
                                             'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn',
                                             'okopf', 'okopf_code', 'okfs', 'okfs_code')
                        df = pd.DataFrame(list(query), columns=invention_bd_excel())
                        df2 = pd.DataFrame(list(query2), columns=pmodels_bd_excel())
                        df3 = pd.DataFrame(list(query3), columns=prom_bd_excel())
                        df['registration date'] = pd.to_datetime(df['registration date'])
                        df['expiration date'] = pd.to_datetime(df['expiration date'])
                        df = pd.concat([df, df2, df3])
                        df['registration date'] = df['registration date'].dt.strftime('%Y-%m-%d')
                        df['expiration date'] = df['expiration date'].dt.strftime('%Y-%m-%d')
                        name_suffix = '{:%Y%m%d}'.format(datetime.datetime.today()) + str(random.randint(0, 100))
                        filename = f'{name_suffix}.xlsx'
                        path_to_file = os.path.join(BASE_DIR, 'reports/' + filename)
                        Reports.objects.create(invention_bd=invention_bd, pmodels_bd=pmodels_bd,
                                               prom_bd=prom_bd,
                                               start_date=start_date, end_date=end_date, inn=inn, okopf=okopf,
                                               okopf_code=okopf_code, file=filename)
                        df.to_excel(path_to_file)
                        return FileResponse(open(path_to_file, 'rb'))

class Filter_history_report(APIView):
    def get(self, request):
        file_id = self.request.query_params.get('id')
        filename = Reports.objects.filter(id__in=file_id).values('id', 'file')[0]
        file_path = os.path.join(BASE_DIR, 'reports/' + filename['file'])
        response = FileResponse(open(file_path, 'rb'))
        return response


class ReportGetBD(APIView):
    def get(self,request):
        query2 = Invention_bd.objects.all().values_list('registration_number', 'registration_date',
                                                        'application_number',
                                                        'application_date', 'authors', 'authors_latin',
                                                        'patent_holders',
                                                        'patent_holders_latin', 'correspondence_address',
                                                        'correspondence_address_latin', 'invention_name',
                                                        'patent_starting_date', 'crimean_invention_application_number',
                                                        'crimean_invention_application_date',
                                                        'crimean_invention_patent_number_in_ukraine',
                                                        'receipt_date_of_additional_data_to_application',
                                                        'date_of_application_to_wich_additional_data_has_been_received',
                                                        'number_of_application_to_wich_additional_data_has_been_received',
                                                        'initial_application_number', 'initial_application_date',
                                                        'initial_application_priority_date',
                                                        'previous_application_number',
                                                        'previous_application_date', 'paris_convention_priority_number',
                                                        'paris_convention_priority_date',
                                                        'paris_convention_priority_country',
                                                        'pct_application_examination_start_date',
                                                        'pct_application_number',
                                                        'pct_application_date', 'pct_application_publish_number',
                                                        'pct_application_publish_date', 'ea_application_number',
                                                        'ea_application_date', 'ea_application_publish_number',
                                                        'ea_application_publish_date', 'application_publish_date',
                                                        'application_publish_number', 'patent_grant_publish_date',
                                                        'patent_grant_publish_number', 'revoke_patent_number',
                                                        'information_about_the_obligation', 'expiration_date',
                                                        'invention_formula_numbers_for_which_patent_term_is_prolonged',
                                                        'additional_patent', 'actual', 'mpk', 'unnamed_46',
                                                        'unnamed_47',
                                                        'unnamed_48', 'head_or_branch', 'id_child', 'inn', 'is_active',
                                                        'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code')
        df2 = pd.DataFrame(list(query2), columns=invention_bd_excel())
        df2['registration date'] = pd.to_datetime(df2['registration date'])
        df2['expiration date'] = pd.to_datetime(df2['expiration date'])
        df2['registration date'] = df2['registration date'].dt.date
        df2['expiration date'] = df2['expiration date'].dt.date
        path_to_file2 = os.path.join(BASE_DIR, 'full_bd/База по изобретениям.xlsx')
        import xlsxwriter
        workbook = xlsxwriter.Workbook(path_to_file2, {'constant_memory': True, 'strings_to_urls': False})
        worksheet1 = workbook.add_worksheet()
        columns = invention_bd_excel()
        for col in range(len(columns)):
            worksheet1.write(0, col, columns[col])
        for row in range(1, len(df2) + 1):
            for col in range(0, len(df2.columns)):
                try:
                    worksheet1.write(row, col, df2.iloc[row, col])
                except:
                    worksheet1.write(row, col, '')
        workbook.close()
        query1 = Prom_bd.objects.all().values_list('registration_number', 'registration_date', 'application_number',
                                                   'application_date', 'authors', 'authors_latin', 'patent_holders',
                                                   'patent_holders_latin', 'correspondence_address',
                                                   'correspondence_address_latin', 'industrial_design_name',
                                                   'patent_starting_date',
                                                   'crimean_industrial_design_application_number',
                                                   'crimean_industrial_design_application_date',
                                                   'crimean_industrial_design_patent_number_in_ukraine',
                                                   'receipt_date_of_additional_data_to_application',
                                                   'date_of_application_to_wich_additional_data_has_been_received',
                                                   'number_of_application_to_wich_additional_data_has_been_received',
                                                   'initial_application_number', 'initial_application_date',
                                                   'initial_application_priority_date', 'previous_application_number',
                                                   'previous_application_date',
                                                   'paris_convention_priority_number', 'paris_convention_priority_date',
                                                   'paris_convention_priority_country',
                                                   'patent_grant_publish_date', 'patent_grant_publish_number',
                                                   'revoke_patent_number',
                                                   'expiration_date', 'numbers_of_list_of_essential_features',
                                                   'industrial_designs_names_and_number',
                                                   'actual', 'publication_url', 'actual_date', 'mkpo', 'head_or_branch',
                                                   'id_child', 'inn', 'is_active', 'ogrn', 'okfs', 'okfs_code',
                                                   'okopf', 'okopf_code')
        df1 = pd.DataFrame(list(query1), columns=prom_bd_excel())
        df1['registration date'] = pd.to_datetime(df1['registration date'])
        df1['expiration date'] = pd.to_datetime(df1['expiration date'])
        df1['registration date'] = df1['registration date'].dt.date
        df1['expiration date'] = df1['expiration date'].dt.date
        path_to_file1 = os.path.join(BASE_DIR, 'full_bd/База по промышленным образцам.xlsx')
        workbook = xlsxwriter.Workbook(path_to_file1, {'constant_memory': True, 'strings_to_urls': False})
        worksheet1 = workbook.add_worksheet()
        columns = prom_bd_excel()
        for col in range(len(columns)):
            worksheet1.write(0, col, columns[col])
        for row in range(1, len(df1) + 1):
            for col in range(0, len(df1.columns)):
                try:
                    worksheet1.write(row, col, df1.iloc[row, col])
                except:
                    worksheet1.write(row, col, '')
        workbook.close()
        query3 = PModels_bd.objects.all().values_list('registration_number', 'registration_date', 'application_number',
                                                      'application_date', 'authors', 'authors_latin', 'patent_holders',
                                                      'patent_holders_latin', 'correspondence_address',
                                                      'correspondence_address_latin', 'utility_model_name',
                                                      'patent_starting_date', 'crimean_utility_application_number',
                                                      'crimean_utility_application_date',
                                                      'crimean_utility_patent_number_in_ukraine',
                                                      'receipt_date_of_additional_data_to_application',
                                                      'date_of_application_to_wich_additional_data_has_been_received',
                                                      'number_of_application_to_wich_additional_data_has_been_received',
                                                      'initial_application_number', 'initial_application_date',
                                                      'initial_application_priority_date',
                                                      'previous_application_number',
                                                      'previous_application_date', 'paris_convention_priority_number',
                                                      'paris_convention_priority_date',
                                                      'paris_convention_priority_country',
                                                      'pct_application_examination_start_date',
                                                      'pct_application_number',
                                                      'pct_application_date', 'pct_application_publish_number',
                                                      'pct_application_publish_date', 'patent_grant_publish_date',
                                                      'patent_grant_publish_number', 'revoke_patent_number',
                                                      'expiration_date',
                                                      'utility_formula_numbers_for_which_patent_term_is_prolonged',
                                                      'actual', 'publication_url', 'mpk', 'unnamed_39', 'unnamed_40',
                                                      'head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn', 'okfs',
                                                      'okfs_code', 'okopf', 'okopf_code')
        df3 = pd.DataFrame(list(query3), columns=pmodels_bd_excel())
        df3['registration date'] = pd.to_datetime(df3['registration date'])
        df3['expiration date'] = pd.to_datetime(df3['expiration date'])
        df3['registration date'] = df3['registration date'].dt.date
        df3['expiration date'] = df3['expiration date'].dt.date
        path_to_file3 = os.path.join(BASE_DIR, 'full_bd/База по полезным моделям.xlsx')
        workbook = xlsxwriter.Workbook(path_to_file3, {'constant_memory': True, 'strings_to_urls': False})
        worksheet1 = workbook.add_worksheet()
        columns = pmodels_bd_excel()
        for col in range(len(columns)):
            worksheet1.write(0, col, columns[col])
        for row in range(1, len(df3) + 1):
            for col in range(0, len(df3.columns)):
                try:
                    worksheet1.write(row, col, df3.iloc[row, col])
                except:
                    worksheet1.write(row, col, '')
        workbook.close()
        zip_path = os.path.join(BASE_DIR, "full_bd/Вся база патентов.zip")
        with zipfile.ZipFile(zip_path, mode='w') as zf:
            zf.write(os.path.join(BASE_DIR, 'full_bd/База по изобретениям.xlsx'))
            zf.write(os.path.join(BASE_DIR, 'full_bd/База по полезным моделям.xlsx'))
            zf.write(os.path.join(BASE_DIR, 'full_bd/База по промышленным образцам.xlsx'))
        response = FileResponse(open(zip_path, 'rb'))
        return response

class Visualisation(APIView): # Сделать этот метод эффективней путем создания отдельной бд
    def get(self, request):
        report_id = self.request.query_params.get('id', None)
        if report_id is not None:
            reports_query = Reports.objects.get(id=report_id)
            serializer = ReportsSerializer(reports_query)
            file_path = os.path.join(BASE_DIR, 'reports/' + serializer.data['file'])
            df = pd.read_excel(file_path)
            df['registration date'] = pd.to_datetime(df['registration date'])
            df['YearMonth'] = df['registration date'].map(lambda dt: dt.replace(day=1))
            df2 = df.groupby(df["YearMonth"])['registration number'].count()
            obj_list = []
            for i, r in df2.items():
                obj_list.append({"time":'{:%Y-%m-%d}'.format(i), "sum":str(r)})
            return Response(obj_list)
