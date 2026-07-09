# api-automation-tests — Postman, который не спит

[![API Tests](https://github.com/r0meo-1/api-automation-tests/actions/workflows/api-tests.yml/badge.svg)](https://github.com/r0meo-1/api-automation-tests/actions/workflows/api-tests.yml)
![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?logo=postman&logoColor=white)
![Newman](https://img.shields.io/badge/Newman-CLI-FF6C37)
![Node.js](https://img.shields.io/badge/Node.js-20-339933?logo=node.js&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

> «У меня в Postman всё зелёное» — фраза, после которой CI обычно смеётся.  
> Здесь зелёное **и** в Postman, **и** в GitHub Actions. Дважды зелёное. Почти как матрица, только про JSON.

Автотесты **REST API** для сценариев бронирования/оплаты:  
коллекция Postman → прогон **Newman** → отчёт в CI. Smoke, позитив, негатив, идемпотентность, JSON Schema.

Часть QA-портфолио: **[r0meo1.ru](https://r0meo1.ru)** · Роман Неклюдов

---

## Что внутри (без воды)

| Путь | Зачем |
|------|--------|
| `postman/booking-api.postman_collection.json` | 9 запросов, ~20 assertions — основной удар |
| `postman/booking-api.postman_environment.json` | `baseUrl` и прочие мелочи судьбы |
| `docs/api-test-cases.md` | Те же кейсы таблицей — для людей, которые не открывают Postman «на ночь» |
| `.github/workflows/api-tests.yml` | CI: Node → deps → Newman → JUnit |

---

## Покрытие

| Группа | Что проверяем |
|--------|----------------|
| **Smoke** | Жив ли API, `Content-Type`, SLA по времени (да, 30 секунд — это уже не «чуть подтормаживает») |
| **Positive** | GET + schema, POST 201, PUT 200, DELETE 200, фильтры |
| **Negative** | 404 на призраков и кривые маршруты |
| **Idempotency** | Повторное чтение не должно устраивать лотерею |

Итого: **20 assertions**. Все зелёные в CI. Пока. (Спойлер: API меняется. Тесты — ваша страховка.)

---

## Запуск

```bash
npm ci
npm test
```

Или по-старинке:

```bash
npx newman run postman/booking-api.postman_collection.json \
  -e postman/booking-api.postman_environment.json
```

---

## Бэкенд для CI

Чтобы не тащить в CI «настоящий» продовый API (и не устроить DDoS по привычке),  
используется стабильный [JSONPlaceholder](https://jsonplaceholder.typicode.com)  
(заявки → `posts`, клиенты → `users`).  
Структура проверок — как у платёжно-бронировочных интеграций в реальной жизни, только без слёз бухгалтерии.

---

## Стек

`REST` · `Postman` · `Newman` · `JSON Schema` · `Node.js` · `GitHub Actions`

## Связанные репы

- [data-quality-checks](https://github.com/r0meo-1/data-quality-checks) — когда API сказал «ок», а SQL сказал «лжец»
- [test-design-docs](https://github.com/r0meo-1/test-design-docs) — откуда вообще берутся эти кейсы

## Контакты

- **[r0meo1.ru](https://r0meo1.ru)** · [@r0meo1](https://t.me/r0meo1) · r0meo1@ya.ru

## Лицензия

[MIT](LICENSE) — гоняйте тесты, не гоняйте прод без staging.
