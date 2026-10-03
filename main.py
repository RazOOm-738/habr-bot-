import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, CHANNEL_ID
from parser import get_habr_news

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот запущен. Пиши /post для публикации")


@dp.message(Command("post"))
async def post(message: types.Message):
    await bot.send_message(CHANNEL_ID, "Тестовый пост из бота!")
    await message.answer("Пост опубликован")

@dp.message(Command("parse"))
async def parse(message: types.Message):
    await message.answer("Собираю новости...")

    news = await asyncio.to_thread(get_habr_news, 3)

    for n in news:
        text = f"📰 {n['article']}\n\n🔗 {n['link']}"
        await bot.send_message(CHANNEL_ID, text)
        await asyncio.sleep(1)  # пауза между постами

    await message.answer(f"Опубликовано {len(news)} новостей")

async def daily_parse():
    news = await asyncio.to_thread(get_habr_news, 3)
    for n in news:
        text = f"📰 {n['article']}\n\n🔗 {n['link']}"
        await bot.send_message(CHANNEL_ID, text)
        await asyncio.sleep(1)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_parse, "cron", hour=10, minute=0)
    scheduler.start()

    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())