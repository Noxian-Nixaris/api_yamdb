# api_yamdb

## Описание.

Проект API для сайта с Произведениями, отзывами и комментариями.

## Стек использованных технологий:
Django
Django REST Framework

## Установка.

```
git clone https://https://github.com/Noxian-Nixaris/api_yamdb.git
```
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```
##Примеры.
Открыть документацию проекта:
```
/redoc/
```

###Зареоистрировать пользователя:
POST
```
api/v1/auth/signup/
```
```
{
  "email": "user@example.com",
  "username": "^w\\Z"
}
```
Получить токен:
POST
```
/api/v1/auth/token/
```
```
{
"username": "^w\\Z",
"confirmation_code": "string"
}
```

###Получить список произведений.
GET
```
/api/v1/titles/
```
Добавить произведение:
POST
```
/api/v1/titles/
```
```
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```
Получить/Удалить произведение:
GET/DELETE
```
/api/v1/titles/{titles_id}/
```

###Получить список отзывов к произведению:
GET
```
/api/v1/titles/{title_id}/reviews/
```
Написать отзыв:
POST
```
/api/v1/titles/{title_id}/reviews/
```
```
{
"text": "string",
"score": 1
}
```
Получить/Удалить отзыв:
GET/DELETE
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```

###Получить список комментариев:
GET
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Написать комментарий:
POST
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
{
"text": "string"
}
```
Получить/Удалить комментарий:
GET/DELETE

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

##Авторы:
Виктор Желтов
Владимир Рубец
Егор Лазарев
