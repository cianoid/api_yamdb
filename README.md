# api_yamdb
api_yamdb

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


### Важные моменты

1. Если планируете работать с основной веткой, то не забывайте делать 
**git pull** чтобы забрать последние изменения

2. Не стоит пушить в основную ветку файлы миграций. Это может вызвать 
конфликты. Намного проще, если мы будем создавать файлы миграции 
на ветке master после всех мержей. Т.е. локально можно создавать и 
выполнять миграции, но в ветку лучше не включать

3. Янедкс.Практикум рекомендует использовать Python 3.7. Давайте не 
будем отходить от этой рекомендации
