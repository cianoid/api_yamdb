# api_yamdb
api_yamdb

## Подготовка проекта

### Клонирование и подготовка venv
```
git clone https://github.com/cianoid/api_yamdb
python -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
```

### Созданине .env-файла
Для работы требуется .env файл, расположенный на одном уровне 
с файлом README.md.
Нужно создать файл по шаблону

```
SECRET_KEY=some_secret_key
```

### Важные моменты

Если планируете работать с основной веткой, то не забывайте делать
```
git pull
```
чтобы забрать последние изменения