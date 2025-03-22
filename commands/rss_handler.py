import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from services import rss_service

polling_task = None
category = "Angular"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global polling_task
    await db.add_chat_id(update.message.chat_id)
    await update.message.reply_text('Started reading RSS feed...')
    if polling_task is None:
        polling_task = asyncio.create_task(rss_service.poll_rss_updates(context.bot, category))

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global polling_task
    await db.remove_chat_id(update.message.chat_id)
    await update.message.reply_text('Stopped reading RSS feed...')
    if polling_task:
        polling_task.cancel()
        polling_task = None

async def check_url_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(rss_service.RSS_URL + category)
    await update.message.reply_text(rss_service.DOU_RSS_URL)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global category, polling_task
    text = update.message.text.lower()
    change_keyword = "change to"
    change_index = text.find(change_keyword)

    if change_index != -1:
        new_category = text[change_index + len(change_keyword):].strip()
        if new_category and new_category != category:
            category = new_category
            if polling_task:
                polling_task.cancel()
                polling_task = None
            polling_task = asyncio.create_task(rss_service.poll_rss_updates(context.bot, new_category))
            await update.message.reply_text(f"I have changed to {new_category}...")
        else:
            await update.message.reply_text(f"Already monitoring {new_category}...")
    else:
        await update.message.reply_text("I do not understand you...")
