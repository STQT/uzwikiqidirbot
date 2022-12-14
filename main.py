import hashlib

from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, Message
from urllib.parse import quote
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from configs import BOT_TOKEN
from contrib import WikiApi

API_TOKEN = BOT_TOKEN

wiki = WikiApi()

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

help_text = ("Botdan foydalanish uchun @uzwikiqidirbot deb yozib "
             "keyin kerakli maqola nomini yozing")


@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(switch_inline_query="Vikipediya", text="Qidirib ko'rish"))
    return await message.answer("Siz botdan foydalanishingiz mumkin!\n"
                                "Yaratuvchi: @kaireke_sultan", reply_markup=kb)


@dp.message_handler()
async def echo(message: Message):
    if message.chat.type == 'private':
        await message.answer(help_text)


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    items = []
    if inline_query:
        searched_text_list = await wiki.search_by_query(inline_query.query or None)
        for i in searched_text_list:
            url = "[" + i + "]" + "(https://uz.wikipedia.org/wiki/" + quote(i) + ")"
            input_content = InputTextMessageContent(url, parse_mode="Markdown")
            result_id: str = hashlib.md5(i.encode()).hexdigest()

            item = InlineQueryResultArticle(

                id=result_id,

                title=f'Natija {i!r}',

                input_message_content=input_content,

            )
            items.append(item)
    else:
        items.append("Bironta maqola yo'q")

    # don't forget to set cache_time=1 for testing (default is 300s or 5m)

    await bot.answer_inline_query(inline_query.id, results=items)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
