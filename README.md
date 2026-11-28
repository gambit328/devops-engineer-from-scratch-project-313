# Деплой приложения на PaaS (Devops)

[![hexlet-check](https://github.com/gambit328/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/gambit328/devops-engineer-from-scratch-project-313/actions)
[![ci](https://github.com/gambit328/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/gambit328/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml)

Создайте и задеплойте веб-приложение, подключите базу данных и настройте мониторинг ошибок

Учебный проект Хекслета: <https://ru.hexlet.io/programs/devops-engineer-from-scratch>

## Стек

- Python 3.11
- Flask
- SQLModel + PostgreSQL
- React Admin (UI-пакет от Hexlet)
- Docker
- Render
- Bugsink

## Установка

- uv
- make
- Node.js 20.19+ или 22.12+ (для сборки UI)

```bash
git clone https://github.com/gambit328/devops-engineer-from-scratch-project-313.git
cd devops-engineer-from-scratch-project-313

make build
```

### Переменные окружения

- DATABASE_URL (строка подключения к postgresql)
- BASE_URL (публичный адрес приложения. нужен для short_url)
- SENTRY_DSN (DSN из Bugsink для мониторинга)

## Использование

```bash
make run
```

Приложение: <https://devops-engineer-from-scratch-project-313-61xr.onrender.com>

![Bugsink event](screenshots/bugsink-event.png)

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
