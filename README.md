# Проект 15 спринта _INFRA_SP2_
В данном проекте разворачиваем api_yamdb в docker

## Функционал api_yamdb:
Регистрация, создание и редактирование постов, добавление изображения, комментирование. Используется пагинация 
постов, кэширование главной страницы.

### наполнение .env 

```
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db
DB_PORT=5432
```

### Запуск приложения

* Установить Docker для своей ОС
* Перейти в директорию 
    ```
    ~/infra_sp2/infra
    ```
* Выполнить команду
    ```
    docker-compose up -d --build
* Наполнить БД 
    ```
    docker-compose exec web python manage.py migrate
    ```
* Создать суперпользователя
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
* Собрать статические файлы в проекте
    ```
    docker-compose exec web python manage.py collectstatic
    ```
    
<!-- ![yamdb_workflow](https://github.com/sproggi/yamdb_final/action/workflows/yamdb_workflow.yml/badge.svg) -->
![example workflow](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)