import os
from datetime import datetime

import aiohttp
from dotenv import load_dotenv


load_dotenv()


TOKEN_API_MEDIASTACK = os.getenv("TOKEN_API_MEDIASTACK")
URL_API_MEDIASTACK = os.getenv("URL_API_MEDIASTACK")
TELEGRAM_GROUP_LINK = os.getenv("TELEGRAM_GROUP_LINK")

LANGUAGES = os.getenv("LANGUAGES")
KEYWORDS = os.getenv("KEYWORDS")
SOURCES = os.getenv("SOURCES")
SORT = os.getenv("SORT")
LIMIT = min(100, int(os.getenv("LIMIT")))


async def fetch_news_with_pagination(url, params, total):
    try:
        offset = 0
        is_finished = False
        async with aiohttp.ClientSession() as session:
            while not is_finished:
                params.update({"offset": offset})
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data.get("data"):
                        yield data
                    else:
                        is_finished = False
                        break
                offset += LIMIT
                if offset >= total:
                    is_finished = True
                else:
                    is_finished = False
    except Exception as error_pagination:
        print(f"Помилка в etch_news_with_pagination: {error_pagination}")


async def get_news():
    try:
        today = datetime.now().date()
        params = {
            "access_key": TOKEN_API_MEDIASTACK,
            "sort": SORT,
            # "sources": SOURCES,
            "date": today.strftime("%Y-%m-%d"),
            "languages": LANGUAGES,
            "keywords": KEYWORDS,
            "limit": LIMIT,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(URL_API_MEDIASTACK, params=params) as response:
                response.raise_for_status()
                news = await response.json()
                if news.get("data"):
                    pagination = news.get("pagination")
                    total = pagination.get("total")
                    print(f"Загальна к-ть новин:{total}")

                    return fetch_news_with_pagination(
                        URL_API_MEDIASTACK,
                        params,
                        total
                    )
                else:
                    return None

    except Exception as error_get_news:
        print(f"Помилка get_news: {error_get_news}")
