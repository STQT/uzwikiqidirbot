import hashlib

from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, Message

from configs import BOT_TOKEN
from contrib import WikiApi

API_TOKEN = BOT_TOKEN

wiki = WikiApi()

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    return await message.answer("Siz botdan foydalanishingiz mumkin!\n"
                                "Yaratuvchi: @kaireke_sultan")


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    items = []
    if inline_query:
        searched_text_list = await wiki.search_by_query(inline_query.query or None)
        for i in searched_text_list:
            b = "[[" + i + "]]"
            input_content = InputTextMessageContent(b)
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
