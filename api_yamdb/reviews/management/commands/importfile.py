import codecs
import csv
from datetime import datetime as dt

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews import models

model_names = {
    'category': 'Category',
    'comments': 'Comment',
    'genre_title': 'Title',
    'genre': 'Genre',
    'review': 'Review',
    'titles': 'Title',
    'users': 'User',
}

int_fields = ['year', 'pub_date', 'category', 'genre', 'author', 'score']

files = ['category.csv', 'genre.csv', 'titles.csv', 'users.csv',
         'genre_title.csv', 'review.csv', 'comments.csv']


class Command(BaseCommand):
    help = 'Import csv file'
    print(models.Title)

    def handle(self, *args, **options):
        for file in files:
            file_name = file.partition('.')[0]
            path = f'static/data/{file}'
            with codecs.open(path, encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)

                """ Исключение - файл не имеющий собственной модели """
                if file == 'genre_title.csv':
                    for row in reader:
                        title = get_object_or_404(models.Title, id=row[1])
                        title.genre.add(
                            get_object_or_404(models.Genre, id=row[2]))

                ''' Определение имен для орм команды '''
                model = model_names[f'{file_name}']
                method = 'create'

                ''' Определение полей указываемых в модели'''
                for row in reader:
                    fields = ''
                    string_orm = ''
                    for header, field in zip(headers, row):
                        if 'id' in header or header in int_fields:
                            if header in ['category', 'genre', 'author']:
                                header += '_id'
                        elif header == 'text':
                            textfield = f'"{field}"'
                            textfield  # Для прохождения тестов
                            fields += f'{header}=textfield, '
                            continue
                        else:
                            field = f'"{field}"'
                        if header == 'pub_date':
                            datefield = dt.strptime(
                                field, '%Y-%m-%dT%H:%M:%S.%fZ')
                            datefield  # Для прохождения тестов
                            fields += f'{header}=datefield, '
                            continue
                        fields += f'{header}={field}, '
                    fields = fields[:-2]  # Удаление последней запятой
                    string_orm = f'models.{model}.objects.{method}({fields})'
                    print(string_orm)
                    exec(string_orm)
