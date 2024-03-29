Исследоование показало, что ClickHouse быстрее справляется с аналитическими запросами, чем Vertica.
Для примера сравним скорость выполнения одинаковых запросов в обеих БД.

#### Тестирование вставки по 500 записей

- ClickHouse - 1.75 s (1 млн)
- Vertica - 196 s (1 млн)

#### Тестирование одной вставки

- ClickHouse - 8.5 ms (1 млн)
- Vertica - 160 s (1 млн)

#### Тестирование получения данных по uuid (100 Шт.)

    f"SELECT * FROM compare.views where user_id='{u}'"

- ClickHouse - 1.09 s
- Vertica - 0.9 s

Операции вставки 1 млн. записей по одной и пачками в Vertica занмиает значительное время (минуты) по сравнению с CLickouse (та же
операция занимает секунды).

## Вывод

Было решено использовать ClickHouse, так как он быстрее справляется с задачами вставки и агрегации.
