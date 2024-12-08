import aiohttp


from api_mediastack import TELEGRAM_GROUP_LINK
from news_manager import NewsManager


async def check_link(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                return response.status == 200
    except aiohttp.ClientError as error_link:
        print(f"Помилка перевірки посилання {link}: {error_link}")
        return False


async def get_unique_news(news):
    try:
        file_path = "seen_titles.json"
        news_manager = NewsManager(file_path)
        unique_news = []
        for article in news.get("data"):
            title = article.get("title")
            if news_manager.is_new_title(title):
                news_manager.save_title(title)
                description = article.get("description")
                source = article.get("source", None)
                url = article.get("url", "#")
                image_url = article.get("image", None)

                news_item = {
                    "text": (
                        f'<b>"{title}"</b>\n\n'
                        f"{description}\n\n"
                        f'<i>Джерело:</i><a href="{url}"> {source}</a>\n\n'
                        f'<i><u><a href="{TELEGRAM_GROUP_LINK}">Підписатися на TechNova-News</a></u></i>'
                    ),
                    "image": image_url,
                }

                unique_news.append(news_item)
        return unique_news
    except Exception as uniqueness_error:
        print(f"Помилка get_unique_news: {uniqueness_error}")
