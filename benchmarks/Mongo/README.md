Исследование MongoDB
### Развертывание
- `docker-compose up -d --build` - развертывание кластера MongoDB
- `init_mongo.bat` - настройка кластера MongoDB
- `pip install -r requirements.txt` - установка необходимых зависимостей

#### Тестирование
#### Чтение(500 записей)

- чтение списка рецензий к фильму - 0.1115103006362915 s
- чтение списка понравившихся пользователю фильмов - 0.10043874979019166 s
- чтение списка закладок пользователя - 0.009448719024658204 s

#### Запись(batch 1-5000 записей)

- запись списка рецензий к фильму - 0.008768820762634277 s - 0.18363018035888673 s
- запись списка понравившихся пользователю фильмов - 0.009448719024658204 s - 0.13036906719207764 s
- запись списка закладок пользователя - 0.007299375534057617 s - 0.12794137001037598 s

## Вывод

Во всех сценариях использования MongoDB удовлетворяет требованиям производительности  (для операций записи-чтения 200 ms)


### Применяемая схема данных
БД разделена на следующие коллекции:

- **movies**
    - схема данных:
            {
                "_id": <uuid_string>,
                "ratings_qty": <integer>,
                "ratings_sum": <integer>,
                "reviews": [<uuid_string>, ...]
            }
    - не шардируется

- **users**
    - схема данных:
            {
                "_id": <uuid_string>,
                "bookmarks": [<uuid_string>, ...]
            }
    - ключ шардирования: **_id**

- **movie_ratings**
    - схема данных:
            {
                "_id": <uuid_string>,
                "movie_id": <uuid_string>,
                "user_id": <uuid_string>,
                "score": <integer>
            }
    - ключ шардирования: **user_id**

- **reviews**
    - схема данных:
            {
                "_id": <uuid_string>,
                "author_id": <uuid_string>,
                "movie_id": <uuid_string>,
                "text": <string>,
                "pub_date": <datetime>,
                "movie_rating_id": <uuid_string>,
                "movie_rating_score": <integer>,
                "review_rating_sum": <integer>,
                "review_rating_qty": <integer>,
            }
    - ключ шардирования: **author_id**