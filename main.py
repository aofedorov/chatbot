import aiogram, asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from modules.database import data_base, initiate
from modules.settings import ADMINS, TOKEN, BOOK_FORMAT, PAGINATOR_PAGE
from modules.keyboards import main_kb, cancel_kb, paginator_kb, detail_kb


bot = Bot(TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

initiate()
DB = data_base()



class Statements(StatesGroup):
    edit_faq = State()
    
    find_by_title = State()
    find_by_title_author = State()

    find_by_author = State()
    find_by_isbn = State()


def summ_text(books):
    result = ""

    for book_id in books:
        book = DB.get_book(book_id)
        result += BOOK_FORMAT.format(
            book[1],
            book[2], 
            book[3], 
            book[4]
        )

    return result




# STATE
@dp.message_handler(state=Statements.edit_faq, content_types=[types.ContentType.ANY])
async def state_admin_set_kommersant_user(message, state: FSMContext):
    if message.text == "Отмена":
        await message.reply(
            "Отменено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        await state.finish()
        return
    
    # async with state.proxy() as data:
    #     data['chat_id'] = message.text
    
    DB.update_faq(message.html_text)

    await message.answer(
        "Новый текст установлен",
        reply_markup=main_kb(message['from']['id'] in ADMINS)
    )
    await state.finish()

@dp.message_handler(state=Statements.find_by_title, content_types=[types.ContentType.ANY])
async def state_admin_set_kommersant_user(message, state: FSMContext):
    if message.text == "Отмена":
        await message.reply(
            "Отменено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        await state.finish()
        return

    await message.answer("Идёт поиск...")

    books = DB.get_books()
    print(books)
    result = []

    for book in books:
        print(book)
        if message.text.lower() in book[1].lower():
            result.append(str(book[0]))

    DB.update_store(
        message['from']['id'], 
        ",".join(result)
    )

    user = DB.get_user(message['from']['id'])

    if not user[2]:
        await message.answer(
            "К сожалению, по Вашему запросу ничего не найдено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        
        await state.finish()
        return 

    await message.answer(
        f"<b>Найдёно книг: {len(user[2].split(','))}</b>",
        reply_markup=detail_kb()
    )

    await message.answer(
        summ_text(user[2].split(",")[:PAGINATOR_PAGE]),
        reply_markup=paginator_kb(0, len(user[2].split(",")))
    )

    await state.finish()


@dp.message_handler(state=Statements.find_by_title_author, content_types=[types.ContentType.ANY])
async def state_admin_set_kommersant_user(message, state: FSMContext):
    if message.text == "Отмена":
        await message.reply(
            "Отменено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        await state.finish()
        return

    await message.answer("Идёт поиск...")

    user = DB.get_user(message['from']['id'])

    books = []
    for book in user[2].split(","):
        book = DB.get_book(book)

        if message.text.lower() in book[2].lower():
            books.append(str(book[0]))

    DB.update_store(
        message['from']['id'], 
        ",".join(books)
    )

    user = DB.get_user(message['from']['id'])

    if not user[2]:
        await message.answer(
            "К сожалению, по Вашему запросу ничего не найдено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        
        await state.finish()
        return 

    await message.answer(
        summ_text(user[2].split(",")[:PAGINATOR_PAGE]),
        reply_markup=paginator_kb(0, len(user[2].split(",")))
    )

    await message.answer(
        f"Найдено {len(user[2].split(','))} книг",
        reply_markup=main_kb(message['from']['id'] in ADMINS)
    )

    await state.finish()


@dp.message_handler(state=Statements.find_by_author, content_types=[types.ContentType.ANY])
async def state_admin_set_kommersant_user(message, state: FSMContext):
    if message.text == "Отмена":
        await message.reply(
            "Отменено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        await state.finish()
        return

    await message.answer("Идёт поиск...")

    books = DB.get_books()
    print(books)
    result = []

    for book in books:
        print(book)
        if message.text.lower() in book[2].lower():
            result.append(str(book[0]))

    DB.update_store(
        message['from']['id'], 
        ",".join(result)
    )

    user = DB.get_user(message['from']['id'])

    if not user[2]:
        await message.answer(
            "К сожалению, по Вашему запросу ничего не найдено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        
        await state.finish()
        return 

    await message.answer(
        summ_text(user[2].split(",")[:PAGINATOR_PAGE]),
        reply_markup=paginator_kb(0, len(user[2].split(",")))
    )

    await message.answer(
        f"Найдено {len(user[2].split(','))} книг",
        reply_markup=main_kb(message['from']['id'] in ADMINS)
    )

    await state.finish()


@dp.message_handler(state=Statements.find_by_isbn, content_types=[types.ContentType.ANY])
async def state_admin_set_kommersant_user(message, state: FSMContext):
    if message.text == "Отмена":
        await message.reply(
            "Отменено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        await state.finish()
        return

    await message.answer("Идёт поиск...")

    books = DB.get_books()
    print(books)
    result = []

    for book in books:
        print(book)
        if message.text.lower() == book[3].lower():
            result.append(str(book[0]))

    DB.update_store(
        message['from']['id'], 
        ",".join(result)
    )

    user = DB.get_user(message['from']['id'])

    if not user[2]:
        await message.answer(
            "К сожалению, по Вашему запросу ничего не найдено",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )
        
        await state.finish()
        return 

    await message.answer(
        summ_text(user[2].split(",")[:PAGINATOR_PAGE]),
        reply_markup=paginator_kb(0, len(user[2].split(",")))
    )

    await message.answer(
        f"Найдено {len(user[2].split(','))} книг",
        reply_markup=main_kb(message['from']['id'] in ADMINS)
    )

    await state.finish()


# QUERY
@dp.callback_query_handler()
async def process_callback_buttons(callback_query: types.CallbackQuery):
    print(callback_query.data)
    user = DB.get_user(callback_query.from_user.id)

    data = callback_query.data.split("_")

    if data[0] == 'check':
        await callback_query.answer("Счётчик книг")

    elif data[0] == 'next':
        await bot.send_message(
            callback_query.from_user.id,
            summ_text(user[2].split(",")[int(data[1]): int(data[1])+PAGINATOR_PAGE]),
            reply_markup=paginator_kb(int(data[1]), len(user[2].split(",")))
        )
        
        await bot.delete_message(
            callback_query.from_user.id,
            callback_query.message.message_id
        ) 

        await callback_query.answer("Смена страницы")

# COMMANDS
@dp.message_handler(commands=["start"])
async def start_message(message):
    DB.create_user(message['from']['id'])
    await message.answer(f"<b>Привет, {message['from']['first_name']}</b>\
\nЯ бот библиотекарь.")

    await message.answer(
f"Нужна книга? Не можешь её найти? \
Могу тебе помочь. Я ищу отечественные электронные книги по \
всей библиотеке подписок.\n\
Чтобы начать поиск, просто пришли мне <b>название</b>, <b>автора</b> \
или <b>ISBN</b> книги."        
    )

    await message.answer(
        "Пожалуйста, выберите один из вариантов поиска",
        reply_markup=main_kb(message['from']['id'] in ADMINS)
    )


# MESSAGE
@dp.message_handler(content_types=["text"])
async def send_text(message):
    DB.create_user(message['from']['id'])
    user = DB.get_user(message['from']['id'])


    if message.text == "Поиск по названию":
        await message.answer(
            "Введите название или часть названия книги",
            reply_markup=cancel_kb()
        )
        await Statements.find_by_title.set()

    elif message.text == "Уточнить автора":
        await message.answer(
            "Введите имя или часть имени автора книги",
            reply_markup=cancel_kb()
        )
        await Statements.find_by_title_author.set()

    elif message.text == "Поиск по автору":
        await message.answer(
            "Введите имя или часть имени автора книги",
            reply_markup=cancel_kb()
        )
        await Statements.find_by_author.set()

    elif message.text == "Поиск по ISBN":
        await message.answer(
            "Введите isbn книги",
            reply_markup=cancel_kb()
        )
        await Statements.find_by_isbn.set()

    elif message.text == "Помощь":
        await message.answer("Если у Вас есть вопросы, то Вы можете написать @aofedorov")

    elif message.text == "Часто задаваемые вопросы":
        await message.answer(DB.get_faq())

    elif message.text == "✏️ Часто задаваемые вопросы":
        if message['from']['id'] in ADMINS:
            await message.answer(
                "Введите новый текст для данного пункта",
                reply_markup=cancel_kb()
            )

            await Statements.edit_faq.set()

    else:
        await message.answer(
            "Пожалуйста, выберите один из вариантов поиска",
            reply_markup=main_kb(message['from']['id'] in ADMINS)
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) #, on_startup=on_startup)


