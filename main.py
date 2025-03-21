import asyncio
import feedparser
from telegram import Bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7034331285:AAEYDCx88ZG7gGYd3BrWAl6tbdDqvd1d1ps'
CHAT_ID = '141279468'
RSS_URL = 'https://djinni.co/jobs/rss/?primary_keyword='
DOU_RSS_URL = 'https://jobs.dou.ua/vacancies/feeds/?search=angular&category=Front%20End'

bot = Bot(token=TOKEN)
polling_task = None
category = "Angular"

async def check_for_updates(category: str):
    feed = feedparser.parse(RSS_URL + category)
    feed_dou = feedparser.parse(DOU_RSS_URL)

    if feed.entries:
        entry = feed.entries[0]
        latest_title = entry.title

        if latest_title != check_for_updates.previous_title:
          message = f"New job posted on djini:\n{latest_title}\n{entry.link}"
          await bot.send_message(chat_id=CHAT_ID, text=message)
          check_for_updates.previous_title = latest_title

    if feed_dou.entries:
        entry = feed_dou.entries[0]
        latest_title = entry.title

        if latest_title != check_for_updates.previous_dou_title:
          message = f"New job posted on dou:\n{latest_title}\n{entry.link}"
          await bot.send_message(chat_id=CHAT_ID, text=message)
          check_for_updates.previous_dou_title = latest_title

check_for_updates.previous_title = ''
check_for_updates.previous_dou_title = ''


async def poll_rss(category: str):
    while True:
        await check_for_updates(category)
        await asyncio.sleep(300)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global polling_task
    await update.message.reply_text('Started reading RSS feed...')

    if polling_task is None:
      polling_task = asyncio.create_task(poll_rss("Angular"))

async def check_url_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RSS_URL + category)
    await update.message.reply_text(DOU_RSS_URL)

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global polling_task
    await update.message.reply_text('Stopped reading RSS feed...')

    if polling_task:
      polling_task.cancel()
      polling_task = None

# Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global category, polling_task
    text = update.message.text.lower()
    change_keyword = "change to"
    change_index = text.find(change_keyword)

    if change_index != -1:
        formatted_text = text[change_index + len(change_keyword):].strip()
        category = formatted_text
        if polling_task:
            polling_task.cancel()
            polling_task = None
        polling_task = asyncio.create_task(poll_rss(formatted_text))
        await update.message.reply_text(f"I have changed to {formatted_text}...")
    else:
        await update.message.reply_text("I do not understand you...")

# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting application...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('stop', stop_command))
    app.add_handler(CommandHandler('check_url', check_url_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling()