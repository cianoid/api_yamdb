# api_yamdb

Групповой проект. Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. К произведениям можно оставлять отзывы (текст и рейтинг).

## Подготовка проекта

### Клонирование и подготовка venv
```
git clone https://github.com/cianoid/api_yamdb
python -m venv venv
source venv/scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Созданине .env-файла
Для работы требуется .env файл, расположенный на одном уровне 
с файлом README.md.
Нужно создать файл по шаблону

```
SECRET_KEY=some_secret_key
```

Хоть в задании про это ничего не написано, но это хорошая практика. 
Никакие приватные вещи не должны попадать в репозиторий

### Импорт тестовых данных

Импорт выполняется следующими комаднами в заданном порядке
```
python manage.py wipedata
python manage.py importdata static/data/users.csv User
python manage.py importdata static/data/category.csv Category
python manage.py importdata static/data/genre.csv Genre
python manage.py importdata static/data/titles.csv Title
python manage.py importdata --relation-field genre static/data/genre_title.csv Title
python manage.py importdata static/data/review.csv Review
python manage.py importdata static/data/comments.csv Comment
```

Помощь по команде находится тут
```
python manage.py help importdata
```
