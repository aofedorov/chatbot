from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .settings import PAGINATOR_PAGE

def main_kb(admin):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("Поиск по названию"),
        KeyboardButton("Поиск по автору"),
        KeyboardButton("Поиск по ISBN")
    )

    kb.add(
        KeyboardButton("Помощь"),
        KeyboardButton("Часто задаваемые вопросы")
    )

    if admin:
        kb.add(
            KeyboardButton("✏️ Часто задаваемые вопросы")
        )

    return kb

def detail_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("Уточнить автора")
    )

    kb.add(
        KeyboardButton("В меню")
    )

    return kb

def cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("Отмена")
    )

    return kb


def paginator_kb(current_book, count_books):
    kb = InlineKeyboardMarkup()

    curr = current_book + PAGINATOR_PAGE
    if curr > count_books:
        curr = count_books


    if count_books < PAGINATOR_PAGE:
        kb.add(
            InlineKeyboardButton(
                f"{count_books}",
                callback_data=f"check"
            )
        )

    elif current_book < count_books and curr > PAGINATOR_PAGE and count_books != curr:
        kb.add(
            InlineKeyboardButton(
                "Назад",
                callback_data=f"next_{current_book - PAGINATOR_PAGE}"
            ),

            InlineKeyboardButton(
                f"{curr} / {count_books}",
                callback_data=f"check"
            ),

            InlineKeyboardButton(
                "Далее",
                callback_data=f"next_{current_book + PAGINATOR_PAGE}"
            )
        )


    elif curr > PAGINATOR_PAGE:
        kb.add(
            InlineKeyboardButton(
                "Назад",
                callback_data=f"next_{current_book - PAGINATOR_PAGE}"
            ),

            InlineKeyboardButton(
                f"{curr} / {count_books}",
                callback_data=f"check"
            )
        )

    # кол-во книг больше, чем показанно
    elif current_book < count_books:
        kb.add(
            InlineKeyboardButton(
                f"{curr} / {count_books}",
                callback_data=f"check"
            ),

            InlineKeyboardButton(
                "Далее",
                callback_data=f"next_{current_book + PAGINATOR_PAGE}"
            )
        )
    


    return kb


