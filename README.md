# 🔧 IT Helpdesk - Система управления заявками

Комплексная система для управления заявками на ремонт и обслуживание оргтехники, а также поддержки по программному обеспечению.

## 📋 Возможности

### Для пользователей (Telegram Bot):
- ✅ Создание заявок через удобный интерфейс бота
- ✅ Выбор категории (оборудование/ПО)
- ✅ Установка приоритета
- ✅ Просмотр статуса своих заявок
- ✅ Добавление комментариев
- ✅ Прикрепление фото/скриншотов
- ✅ Уведомления об изменениях

### Для инженеров/админов (Web интерфейс):
- 📊 Просмотр всех заявок с фильтрацией
- 👤 Назначение заявок на себя или коллег
- 🔄 Изменение статусов заявок
- 💬 Комментарии (публичные и внутренние)
- 📝 Полный журнал всех действий
- 📈 Статистика и отчеты
- 🔍 Поиск и фильтрация заявок

## 🏗 Архитектура

```
┌─────────────────┐         ┌──────────────────┐
│  Telegram Bot   │────────▶│   FastAPI API    │
│   (Пользо-      │         │   (Backend)      │
│   ватели)       │         │                  │
└─────────────────┘         │  • REST API      │
                            │  • JWT Auth      │
┌─────────────────┐         │  • WebSocket     │
│  Web Frontend   │────────▶│                  │
│   (Админы/      │         └─────────┬────────┘
│   Инженеры)     │                   │
└─────────────────┘                   │
                                      ▼
                            ┌──────────────────┐
                            │   PostgreSQL     │
                            │   (База данных)  │
                            └──────────────────┘
```

## 🚀 Технологии

### Backend
- **FastAPI** - современный, быстрый веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - реляционная СУБД
- **JWT** - аутентификация и авторизация
- **Pydantic** - валидация данных

### Bot
- **aiogram 3.x** - асинхронная библиотека для Telegram Bot API
- **SQLAlchemy** - работа с БД

### Frontend
- **HTML/CSS/JavaScript** - простой и эффективный интерфейс
- **Vanilla JS** - без зависимостей
- Адаптивный дизайн

### Infrastructure
- **Docker & Docker Compose** - контейнеризация
- **Nginx** - реверс-прокси (опционально)

## 📦 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Telegram Bot Token (от @BotFather)

### Установка

1. **Клонируйте репозиторий:**

```bash
git clone <repository-url>
cd BSME
```

2. **Настройте переменные окружения:**

```bash
cp .env.example .env
nano .env
```

Обязательно измените:
- `TELEGRAM_BOT_TOKEN` - ваш токен бота
- `SECRET_KEY` - случайная строка для JWT
- `POSTGRES_PASSWORD` - пароль БД

3. **Запустите сервисы:**

```bash
docker-compose up -d
```

4. **Инициализируйте базу данных:**

```bash
docker exec -it helpdesk_backend python init_db.py
```

5. **Готово!**

- API: http://localhost:8000/api/docs
- Веб-интерфейс: http://localhost:8000/dashboard
- Telegram Bot: @your_bot_name

### Тестовые учетные записи

После инициализации доступны:

| Роль     | Username   | Password     |
|----------|------------|--------------|
| Admin    | admin      | admin123     |
| Engineer | engineer   | engineer123  |
| User     | user       | user123      |

⚠️ **Важно:** Измените эти пароли в продакшн!

## 📖 Документация

- [Руководство по установке](docs/INSTALLATION.md)
- [API документация](http://localhost:8000/api/docs) - автогенерируется FastAPI
- [Архитектура проекта](CLAUDE.md)

## 🗂 Структура проекта

```
BSME/
├── backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── api/            # REST API endpoints
│   │   ├── core/           # Конфигурация, БД, безопасность
│   │   ├── models/         # SQLAlchemy модели
│   │   └── schemas/        # Pydantic схемы
│   ├── Dockerfile
│   ├── requirements.txt
│   └── init_db.py          # Скрипт инициализации БД
│
├── bot/                     # Telegram Bot
│   ├── main.py             # Главный файл бота
│   ├── keyboards.py        # Клавиатуры
│   ├── config.py           # Конфигурация
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                # Веб-интерфейс
│   ├── templates/          # HTML шаблоны
│   └── static/             # CSS, JS, изображения
│
├── docs/                    # Документация
│   └── INSTALLATION.md
│
├── docker-compose.yml       # Docker Compose конфигурация
├── .env.example            # Пример переменных окружения
├── .gitignore
├── CLAUDE.md               # Руководство для AI
└── README.md               # Этот файл
```

## 🔐 Безопасность

- ✅ JWT токены для аутентификации
- ✅ Bcrypt для хеширования паролей
- ✅ Валидация данных через Pydantic
- ✅ Защита от SQL инъекций (ORM)
- ✅ CORS настройки
- ✅ Разделение ролей (user, engineer, admin)

## 🎯 Основные функции

### Управление заявками

- Создание заявок с детальным описанием
- Категории: Оборудование / Программное обеспечение
- Приоритеты: Критический / Высокий / Средний / Низкий
- Статусы: Новая / В работе / Решена / Закрыта

### Журнал действий

- Автоматическое логирование всех изменений
- История комментариев
- Отслеживание назначений
- Изменения статусов и приоритетов

### Уведомления

- Telegram уведомления при создании заявки
- Уведомления о назначении
- Уведомления об изменении статуса
- Комментарии к заявкам

## 🛠 Разработка

### Запуск в режиме разработки

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Bot:**
```bash
cd bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Тестирование API

Используйте встроенную документацию Swagger:
```
http://localhost:8000/api/docs
```

## 📊 База данных

### Основные таблицы

- `users` - пользователи системы
- `tickets` - заявки
- `comments` - комментарии к заявкам
- `ticket_history` - журнал изменений
- `attachments` - прикрепленные файлы

### Миграции

Для создания новых миграций используйте Alembic:

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта!

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT.

## 👥 Авторы

- Разработка: [Ваше имя]
- Проект создан с помощью Claude AI

## 📞 Поддержка

При возникновении вопросов или проблем:

1. Проверьте [документацию](docs/INSTALLATION.md)
2. Посмотрите [открытые issue](../../issues)
3. Создайте новый issue с подробным описанием проблемы

---

## 🎉 Roadmap

- [ ] Мобильное приложение
- [ ] Email уведомления
- [ ] Интеграция с Active Directory
- [ ] Расширенная статистика и аналитика
- [ ] Экспорт данных в Excel/PDF
- [ ] SLA (Service Level Agreement) трекинг
- [ ] База знаний (Knowledge Base)
- [ ] Чат-бот с AI для автоматических ответов

---

**Сделано с ❤️ для IT поддержки**
