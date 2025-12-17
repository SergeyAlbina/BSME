"""
Скрипт инициализации базы данных
Создает таблицы и добавляет тестовых пользователей
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.database import Base
from app.models import User, Ticket, Comment
from app.core.security import get_password_hash


async def init_db():
    """Инициализация базы данных"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    print("Создание таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Таблицы созданы!")

    # Создание тестовых пользователей
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        # Админ
        admin = User(
            username="admin",
            full_name="Администратор",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role="admin",
        )
        session.add(admin)

        # Инженер
        engineer = User(
            username="engineer",
            full_name="Инженер Иван",
            email="engineer@example.com",
            hashed_password=get_password_hash("engineer123"),
            role="engineer",
        )
        session.add(engineer)

        # Обычный пользователь
        user = User(
            username="user",
            full_name="Пользователь Петр",
            email="user@example.com",
            hashed_password=get_password_hash("user123"),
            role="user",
        )
        session.add(user)

        await session.commit()

    print("\nТестовые пользователи созданы:")
    print("  Admin: username=admin, password=admin123")
    print("  Engineer: username=engineer, password=engineer123")
    print("  User: username=user, password=user123")
    print("\nБаза данных готова к использованию!")


if __name__ == "__main__":
    asyncio.run(init_db())
