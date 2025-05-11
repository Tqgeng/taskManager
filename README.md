# Task Manager - FastAPI + PostgreSQL в Docker

Это веб-приложение для отслеживания списка дел. Использует FastAPI, PostgreSQL и pgAdmin, всё запускается через Docker.

---

## Требования

- Установленный [Docker](https://www.docker.com/)
- Установленный [Docker Compose](https://docs.docker.com/compose/)

---

## Запуск проекта

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Tqgeng/taskManager.git
cd taskManager
```
 
2. Соберите и запустите контейнеры:
```bash
docker compose up --build -d
```

3. Приложение будет доступно по адресу:

API: http://localhost:8000/docs

pgAdmin: http://localhost:5050 (email: admin@admin.org, пароль: admin)
