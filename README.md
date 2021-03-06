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

### Документация по API
```
http://51.250.19.193/redoc/
```
### Админка
```
http://51.250.19.193/admin/
```
### Основной эндпоинт:
```
http://51.250.19.193/api/v1/

![yamdb_final workflow](https://github.com/sproggi/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)