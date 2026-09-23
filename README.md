# api-automation-tests — Postman, который не спит

[![API Tests](https://github.com/r0meo-1/api-automation-tests/actions/workflows/api-tests.yml/badge.svg)](https://github.com/r0meo-1/api-automation-tests/actions/workflows/api-tests.yml)
![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?logo=postman&logoColor=white)
![Newman](https://img.shields.io/badge/Newman-CLI-FF6C37)
![Node.js](https://img.shields.io/badge/Node.js-20-339933?logo=node.js&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

> «У меня в Postman всё зелёное» — фраза, после которой CI обычно смеётся.  
> Здесь зелёное **и** в Postman, **и** в GitHub Actions. Дважды зелёное. Почти как матрица, только про JSON.

Автотесты **REST API и браузерного UI** для сценариев бронирования:
Postman/Newman + Python/pytest + Playwright → раздельные отчёты в CI. Smoke,
позитив, негатив, границы 1–28 ночей, контракт API и пользовательский сценарий.

Часть портфолио: **[r0meo1.ru](https://r0meo1.ru)** · Роман Неклюдов

## За 20 секунд

| | |
|--|--|
| **Что** | Postman-коллекция REST API + Newman в CI |
| **Зачем** | «У меня зелёное» = зелёное и в Actions, не только на ноутбуке |
| **Проверить** | [CI badge](https://github.com/r0meo-1/api-automation-tests/actions) · `npx newman run postman/...` |

---

## Что внутри (без воды)

| Путь | Зачем |
|------|--------|
| `postman/booking-api.postman_collection.json` | 9 сценариев, 10 HTTP-запросов, 22 assertions |
| `postman/booking-api.postman_environment.json` | `baseUrl` и прочие мелочи судьбы |
| `docs/api-test-cases.md` | Те же кейсы таблицей — для людей, которые не открывают Postman «на ночь» |
| `.github/workflows/api-tests.yml` | CI: Node → deps → Newman → JUnit |
| `qa_portfolio/server.py` | Детерминированный локальный API и HTML-форма без зависимости от production |
| `python_tests/api/` | pytest API: контракт, границы, негативные payload и content type |
| `python_tests/ui/` | Playwright: успешное бронирование и серверная ошибка |
| `.github/workflows/python-qa.yml` | Раздельные API/UI jobs, Chromium и JUnit artifacts |

---

## Покрытие

| Группа | Что проверяем |
|--------|----------------|
| **Smoke** | Жив ли API, `Content-Type`, SLA по времени (да, 30 секунд — это уже не «чуть подтормаживает») |
| **Positive** | GET + schema, POST 201, PUT 200, DELETE 200, фильтры |
| **Negative** | 404 на призраков и кривые маршруты |
| **Idempotency** | Повторное чтение не должно устраивать лотерею |

Итого: **22 assertions**. Сценарий повторного чтения отправляет два отдельных
GET-запроса и сравнивает полное JSON-тело, а также проверяет статус второго ответа.

---

## Запуск

```bash
npm ci
npm test
npm run test:contracts
```

Python/pytest + Playwright:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install .
python -m playwright install chromium
python -m pytest
```

Быстрые срезы:

```bash
python -m pytest -m api
python -m pytest -m ui
python -m pytest -m smoke
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

JSONPlaceholder имитирует запись: ответы POST/PUT не доказывают сохранение данных
или работу настоящих платежей. Повторное чтение проверяет стабильность статического
ресурса демонстрационного API, а не идемпотентность создания бронирования.

`npm run test:contracts` запускает Newman против локального HTTP-сервера без внешней
сети. Четыре регрессионных сценария проверяют два фактических запроса, успех при
одинаковых ответах и обнаружение изменённого тела, HTTP 500 и обрыва соединения.

---

## Стек

Состояние зависимостей Newman и оставшиеся предупреждения аудита описаны в
[dependency-status.md](docs/dependency-status.md). Проверки API не заменяют аудит зависимостей.

`REST` · `Postman` · `Newman` · `pytest` · `Playwright` · `Python` · `JSON Schema` · `GitHub Actions`

## Связанные репы

- [data-quality-checks](https://github.com/r0meo-1/data-quality-checks) — когда API сказал «ок», а SQL сказал «лжец»
- [test-design-docs](https://github.com/r0meo-1/test-design-docs) — откуда вообще берутся эти кейсы

## Контакты

- **[r0meo1.ru](https://r0meo1.ru)** · [@r0meo1](https://t.me/r0meo1) · r0meo1@ya.ru

## Лицензия

[MIT](LICENSE) — гоняйте тесты, не гоняйте прод без staging.
