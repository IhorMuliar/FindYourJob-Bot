import asyncio
import feedparser
from database import db
from telegram import Bot

RSS_URL = 'https://djinni.co/jobs/rss/?primary_keyword='
DOU_RSS_URL = 'https://jobs.dou.ua/vacancies/feeds/?search=angular&category=Front%20End'

previous_titles = {
    "djinni": '',
    "dou": ''
}

async def fetch_feed_updates(bot: Bot, category: str):
    try:
        djinni_feed = feedparser.parse(RSS_URL + category)
        dou_feed = feedparser.parse(DOU_RSS_URL)
        chat_ids = await db.get_all_chat_ids()

        if djinni_feed.entries:
            latest_title = djinni_feed.entries[0].title
            if latest_title != previous_titles["djinni"]:
                message = f"New job posted on djinni:\n{latest_title}\n{djinni_feed.entries[0].link}"
                for chat_id in chat_ids:
                    await bot.send_message(chat_id=chat_id, text=message)
                previous_titles["djinni"] = latest_title

        if dou_feed.entries:
            latest_title = dou_feed.entries[0].title
            if latest_title != previous_titles["dou"]:
                message = f"New job posted on dou:\n{latest_title}\n{dou_feed.entries[0].link}"
                for chat_id in chat_ids:
                    await bot.send_message(chat_id=chat_id, text=message)
                previous_titles["dou"] = latest_title
    except Exception as e:
        print(f"Error fetching feeds: {e}")

async def poll_rss_updates(bot: Bot, category: str):
    while True:
        await fetch_feed_updates(bot, category)
        await asyncio.sleep(300)
