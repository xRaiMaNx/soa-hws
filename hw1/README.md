## Запуск

```
docker-compose up
```

Можно запустить с тестером, который отправит всевозможные запросы и выведет к ним ответ

```
docker-compose -f docker-compose.test.yaml up
```
## Отправка запроса вручную

Запрос можно отправить вручную из консольки при помощи netcat, где нужно подставить значение TYPE

Возможные значения: ["native", "xml", "json", "proto", "avro", "yaml", "msgpack", "all"]

Где с all будут выведены всевозможные форматы

```
echo "get_result ${TYPE}" | nc -u -w3 0.0.0.0 2000
```
