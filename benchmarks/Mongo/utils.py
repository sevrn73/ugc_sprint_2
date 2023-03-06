import time
from random import choice, randint
from typing import Callable
from uuid import uuid4

from faker import Faker
from pymongo import MongoClient

LIKE = 1
DISLIKE = 0
START_DATE = "-30d"
END_DATE = "now"
MIN_RATING = 1
MAX_RATING = 10
fake = Faker()

MONGO_HOST = "127.0.0.1"

MONGO_PORT = 27017
MONGO_DB = "ugc_db"

ITERATIONS_NUMBER = 10
USERS_IN_BATCH = 10
OPTIMAL_BATCH_SIZE = 200
TEST_RECORDS_SIZE = 10000

client = MongoClient(MONGO_HOST, MONGO_PORT, connect=True, ssl=False)
# client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0')

mongo_db = client[MONGO_DB]


def fake_like_event(user_id: str = None, film_id: str = None) -> dict:
    """Генерация события like."""
    return {
        "user_id": user_id if user_id else str(uuid4()),
        "film_id": film_id if film_id else str(uuid4()),
        "type": choice([LIKE, DISLIKE]),
        "datetime": fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_review_event(user_id: str = None, film_id: str = None) -> dict:
    """Генерация события review."""
    return {
        "user_id": user_id if user_id else str(uuid4()),
        "film_id": film_id if film_id else str(uuid4()),
        "text": fake.text(),
        "rating": randint(MIN_RATING, MAX_RATING),
        "datetime": fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_bookmark_event(user_id: str = None, film_id: str = None) -> dict:
    """Генерация события bookmark."""
    return {
        "user_id": user_id if user_id else str(uuid4()),
        "film_id": film_id if film_id else str(uuid4()),
        "datetime": fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_batch(event_faker: Callable, user_size: int, batch_size: int) -> list[dict]:
    """Генерация батча событий."""
    users = [str(uuid4()) for _ in range(user_size)]
    return [event_faker(user_id=choice(users)) for _ in range(batch_size)]


def fake_users_batch(event_faker: Callable, users: list, batch_size: int) -> list[dict]:
    """Генерация батча событий с фиксированными юзерами."""
    return [event_faker(user_id=choice(users)) for _ in range(batch_size)]


def test_insert_step(
    faker: Callable,
    collection_name: str,
    batch_size: int,
    iterations: int = ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    collection = mongo_db.get_collection(collection_name)
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, USERS_IN_BATCH, batch_size)
        start = time.time()
        collection.insert_many(batch)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    print(
        f"Statistics for {collection_name} batch_size={batch_size}: batch={mean_batch} sec, "
        f"item={mean_batch/batch_size} sec.",
    )


def test_insert(faker: Callable, collection_name: str) -> None:
    """Тестирование вставки с разным размером батча."""
    batch_sizes = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000]
    for batch_size in batch_sizes:
        test_insert_step(faker, collection_name, batch_size)


def test_read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    statistics = []
    collection = mongo_db.get_collection(collection_name)
    users = [str(uuid4()) for _ in range(users_size)]

    for i in range(0, TEST_RECORDS_SIZE, OPTIMAL_BATCH_SIZE):
        batch = fake_users_batch(faker, users, batch_size=OPTIMAL_BATCH_SIZE)
        collection.insert_many(batch)

    for user in users:
        start = time.time()
        _ = list(collection.find({"user_id": user}))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    print(
        f"Statistics read for {collection_name} for ~{int(TEST_RECORDS_SIZE/users_size)} records: {mean_batch} sec",
    )
