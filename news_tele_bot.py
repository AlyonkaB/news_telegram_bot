import asyncio
import os

from aiogram import Bot
from aiogram.types import URLInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv

from api_mediastack import get_news
from check_news import check_link, get_unique_news

load_dotenv()


TOKEN_API_TELEGRAM_BOT = os.getenv("TOKEN_API_TELEGRAM_BOT")
CHANNEL_ID = os.getenv("CHANNEL_ID")


bot = Bot(token=TOKEN_API_TELEGRAM_BOT)


async def send_news():
    try:
        print("Виконується задача send_news...")
        news_generator = await get_news()
        print("Отримуються новини з генератора новин...")
        if news_generator:
            async for news in news_generator:
                print(f"Новина: {news}")
                unique_news = await get_unique_news(news)
                print("Перевірка сторінки новин на унікальність...")
                if unique_news:
                    for new in unique_news:
                        if new["image"] and await check_link(new["image"]):
                            photo = URLInputFile(url=new["image"])
                            await bot.send_photo(
                                chat_id=CHANNEL_ID,
                                photo=photo,
                                caption=new["text"],
                                parse_mode="HTML",
                            )
                        else:
                            await bot.send_message(
                                chat_id=CHANNEL_ID,
                                text=new["text"],
                                parse_mode="HTML"
                            )
                    print("Новини успішно відправлені.")
                else:
                    print("Унікальних новин для відправки немає.")
                await asyncio.sleep(1)
            print("Задача send_news виконана успішно.")
        else:
            print("Новин для відправки немає. Завершення задачі")
    except Exception as error_send_news:
        print(f"Помилка в send_news: {error_send_news}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_news, "interval", seconds=60)
    scheduler.start()
    print("Планувальник запущено. Натисніть Ctrl+C, щоб вийти.")

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print(f"Програма завершена.")
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error_start:
        print(f"Помилка запуску: {error_start}")
