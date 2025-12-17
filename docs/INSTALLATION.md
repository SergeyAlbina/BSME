# Руководство по установке и развертыванию IT Helpdesk

## Требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)
- Telegram Bot Token (получить у @BotFather)

---

## Быстрый старт с Docker

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd BSME
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и отредактируйте значения:

```bash
cp .env.example .env
nano .env
```

Обязательные изменения:
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `SECRET_KEY` - секретный ключ (сгенерируйте случайную строку)
- `POSTGRES_PASSWORD` - пароль для PostgreSQL

### 3. Запуск всех сервисов

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (порт 5432)
- Backend API (порт 8000)
- Telegram Bot

### 4. Инициализация базы данных

```bash
# Войдите в контейнер backend
docker exec -it helpdesk_backend bash

# Запустите скрипт инициализации
python init_db.py

# Выйдите из контейнера
exit
```

### 5. Проверка работы

- API документация: http://localhost:8000/api/docs
- Веб-интерфейс: http://localhost:8000/dashboard
- Health check: http://localhost:8000/api/health

Тестовые учетные записи:
- **Admin**: username=`admin`, password=`admin123`
- **Engineer**: username=`engineer`, password=`engineer123`
- **User**: username=`user`, password=`user123`

---

## Локальная разработка (без Docker)

### 1. Установка PostgreSQL

Установите PostgreSQL 14+ и создайте базу данных:

```sql
CREATE DATABASE helpdesk_db;
CREATE USER helpdesk WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE helpdesk_db TO helpdesk;
```

### 2. Backend

```bash
cd backend

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Инициализируйте БД
python init_db.py

# Запустите сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Telegram Bot

```bash
cd bot

# Создайте виртуальное окружение (если еще не создано)
python -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите бота
python main.py
```

---

## Настройка Telegram Bot

### 1. Создание бота

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте токен и добавьте в `.env`

### 2. Настройка команд бота

Отправьте @BotFather команду `/setcommands` и выберите вашего бота.
Затем отправьте:

```
start - Начать работу с ботом
help - Помощь по использованию
mytickets - Показать мои заявки
```

### 3. Получение ID администраторов

Для получения вашего Telegram ID:
1. Найдите @userinfobot
2. Отправьте ему любое сообщение
3. Скопируйте ID и добавьте в `.env` в `TELEGRAM_ADMIN_IDS`

---

## Развертывание на продакшн

### На собственном сервере

1. **Установите Docker и Docker Compose**

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose
```

2. **Клонируйте репозиторий**

```bash
git clone <repository-url>
cd BSME
```

3. **Настройте переменные окружения**

```bash
cp .env.example .env
nano .env
```

Важно изменить:
- `SECRET_KEY` - используйте длинную случайную строку
- `DEBUG=False`
- `ENVIRONMENT=production`
- Надежные пароли для PostgreSQL

4. **Настройте nginx (опционально)**

Создайте файл `/etc/nginx/sites-available/helpdesk`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Активируйте конфигурацию:

```bash
sudo ln -s /etc/nginx/sites-available/helpdesk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

5. **SSL сертификат с Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

6. **Запустите сервисы**

```bash
docker-compose up -d
docker exec -it helpdesk_backend python init_db.py
```

7. **Настройте автозапуск**

Docker Compose автоматически перезапустит контейнеры при перезагрузке сервера
благодаря параметру `restart: unless-stopped`.

---

## Управление сервисами

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Только bot
docker-compose logs -f bot
```

### Остановка сервисов

```bash
docker-compose stop
```

### Перезапуск сервисов

```bash
docker-compose restart
```

### Обновление кода

```bash
git pull
docker-compose build
docker-compose up -d
```

---

## Резервное копирование

### Backup базы данных

```bash
docker exec helpdesk_db pg_dump -U helpdesk helpdesk_db > backup_$(date +%Y%m%d).sql
```

### Восстановление из backup

```bash
cat backup_20250101.sql | docker exec -i helpdesk_db psql -U helpdesk helpdesk_db
```

---

## Решение проблем

### База данных не подключается

```bash
# Проверьте статус PostgreSQL
docker-compose ps postgres

# Проверьте логи
docker-compose logs postgres
```

### Бот не отвечает

```bash
# Проверьте статус бота
docker-compose ps bot

# Проверьте логи
docker-compose logs bot

# Проверьте токен в .env
cat .env | grep TELEGRAM_BOT_TOKEN
```

### Backend не запускается

```bash
# Проверьте логи
docker-compose logs backend

# Проверьте переменные окружения
docker exec helpdesk_backend env | grep DATABASE_URL
```

---

## Мониторинг

### Проверка здоровья API

```bash
curl http://localhost:8000/api/health
```

Должен вернуть: `{"status":"healthy"}`

### Мониторинг использования ресурсов

```bash
docker stats
```

---

## Обновление системы

1. Сделайте backup базы данных
2. Остановите сервисы: `docker-compose stop`
3. Получите обновления: `git pull`
4. Пересоберите контейнеры: `docker-compose build`
5. Запустите сервисы: `docker-compose up -d`
6. Проверьте логи: `docker-compose logs -f`

---

## Поддержка

При возникновении проблем:
1. Проверьте логи всех сервисов
2. Убедитесь, что все переменные окружения настроены правильно
3. Проверьте документацию API: http://localhost:8000/api/docs
