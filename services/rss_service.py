import asyncio
import os
import feedparser
from telegram import Bot
from dotenv import load_dotenv

load_dotenv(".env")
chat_id = os.getenv("CHAT_ID")

if not chat_id:
    raise ValueError("Chat ID not found. Please check your .env file.")

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

        if djinni_feed.entries:
            latest_title = djinni_feed.entries[0].title
            if latest_title != previous_titles["djinni"]:
                message = f"New job posted on djinni:\n{latest_title}\n{djinni_feed.entries[0].link}"
                await bot.send_message(chat_id=chat_id, text=message)
                previous_titles["djinni"] = latest_title

        if dou_feed.entries:
            latest_title = dou_feed.entries[0].title
            if latest_title != previous_titles["dou"]:
                message = f"New job posted on dou:\n{latest_title}\n{dou_feed.entries[0].link}"
                await bot.send_message(chat_id=chat_id, text=message)
                previous_titles["dou"] = latest_title
    except Exception as e:
        print(f"Error fetching feeds: {e}")

async def poll_rss_updates(bot: Bot, category: str):
    while True:
        await fetch_feed_updates(bot, category)
        await asyncio.sleep(300)
