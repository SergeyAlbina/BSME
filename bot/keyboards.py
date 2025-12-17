from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать заявку")],
            [KeyboardButton(text="📋 Мои заявки"), KeyboardButton(text="ℹ️ Помощь")],
        ],
        resize_keyboard=True,
    )
    return keyboard


def category_keyboard():
    """Выбор категории заявки"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖥 Оборудование", callback_data="category:hardware")],
            [InlineKeyboardButton(text="💾 Программное обеспечение", callback_data="category:software")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )
    return keyboard


def priority_keyboard():
    """Выбор приоритета заявки"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔴 Критический", callback_data="priority:critical")],
            [InlineKeyboardButton(text="🟠 Высокий", callback_data="priority:high")],
            [InlineKeyboardButton(text="🟡 Средний", callback_data="priority:medium")],
            [InlineKeyboardButton(text="🟢 Низкий", callback_data="priority:low")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )
    return keyboard


def ticket_action_keyboard(ticket_id: int):
    """Действия с заявкой"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Добавить комментарий", callback_data=f"comment:{ticket_id}")],
            [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh:{ticket_id}")],
        ]
    )
    return keyboard


def cancel_keyboard():
    """Кнопка отмены"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )
    return keyboard
