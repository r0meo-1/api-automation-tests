# qa-api-tests — Postman + Newman API Test Suite

[![API Tests](https://github.com/r0meo-1/api-automation-tests/actions/workflows/api-tests.yml/badge.svg)](https://github.com/r0meo-1/api-automation-tests/actions/workflows/api-tests.yml)
![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?logo=postman&logoColor=white)
![Newman](https://img.shields.io/badge/Newman-CLI-FF6C37)
![Node.js](https://img.shields.io/badge/Node.js-20-339933?logo=node.js&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

> Автоматизированный набор **API-тестов** для REST API системы бронирования/оплаты.
> Postman-коллекция, прогон через **Newman**, непрерывный прогон в **GitHub Actions (CI/CD)**.
>
> Часть QA-портфолио: **[r0meo1.ru](https://r0meo1.ru)** · автор — Роман Неклюдов (Middle QA Engineer).

## Что внутри

- **`postman/booking-api.postman_collection.json`** — 9 запросов, 20 проверок: smoke, позитивные и негативные сценарии, идемпотентность.
- **`postman/booking-api.postman_environment.json`** — окружение с `baseUrl`.
- **`docs/api-test-cases.md`** — тест-кейсы в табличном виде (ID, тип, шаги, ожидаемый результат).
- **`.github/workflows/api-tests.yml`** — CI: устанавливает Node, ставит зависимости, гоняет Newman, публикует JUnit-отчёт.

## Покрытие

| Группа | Проверки |
|--------|----------|
| Smoke | доступность списка, `Content-Type`, время ответа (SLA) |
| Positive | `GET` карточки + JSON Schema, `POST` 201, `PUT` 200, `DELETE` 200, фильтрация по клиенту |
| Negative | 404 на несуществующий ресурс и неизвестный маршрут |
| Idempotency | детерминированность повторного чтения |

Всего: **20 assertions**, все зелёные в CI.

## Запуск локально

```bash
npm ci
npm test
```

Или напрямую через Newman:

```bash
npx newman run postman/booking-api.postman_collection.json \
  -e postman/booking-api.postman_environment.json
```

## Бэкенд

Для воспроизводимого прогона в CI используется публичный стабильный API
[JSONPlaceholder](https://jsonplaceholder.typicode.com) (заявки → `posts`, клиенты → `users`).
Структура проверок повторяет реальные кейсы тестирования платёжно-бронировочных интеграций.

## Стек

`REST API` · `Postman` · `Newman` · `JSON Schema` · `Node.js` · `GitHub Actions` · `CI/CD`

## Контакты

- Сайт / портфолио: **[r0meo1.ru](https://r0meo1.ru)**
- Telegram: [@r0meo1](https://t.me/r0meo1) · Email: r0meo1@ya.ru · GitHub: [r0meo-1](https://github.com/r0meo-1)

## Лицензия

[MIT](LICENSE)
