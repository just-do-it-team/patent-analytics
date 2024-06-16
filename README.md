# Сервис_обработки_патентов_ЛЦТ_2024_1_justdoit

Сервис обработки и аналитики патентов по задаче №1 проекта ЛЦТ 2024 от команды justdoit

### Используемый стек технологий

Frontend:
* Vite
* TypeScript
* React + Redux Toolkit
* CSS modules

Backend:
* Python
* Django + django-rest-framework
* pandas
* PostgresQL
* nginx

### Запуск проекта

Для запуска клиентской части, откройте проект например в VSCode или WebStorm, в терминале перейдите в папку с проектом и выполните следующие команды:

```sh
npm install
npm dev start
```

Проект автоматически запуститься и откроется в браузере, либо вы можете проверить работу запущенного проекта, введя
следующую ссылку в адресную строку бразуера:

```sh
127.0.0.1:5173
```

Для запуска серверной части, откройте проект например в VSCode или PyCharm, в терминале перейдите в папку с проектом и выполните следующие команды:

```sh
python manage.py runserver 127.0.0.1:8000
```

Для разметки патентов использовался pandas, тк поиск по csv-файлу локально оказалось быстрее, чем поиск по бд в postgres

Код используемый для разметки в файлах patent-analytics/backend/mp-test.py и patent-analytics/backend/patent_marking_csv.py

Результаты разметки:
* База промышленных образцов - 4643 из 90193
* База изобретений - 18336 из 222359 (из низ по id физ.лиц - 90)
* База полезных моделей - 44081 из 813608 (из них по id физ.лиц - 5822)