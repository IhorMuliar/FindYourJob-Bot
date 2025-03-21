import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands import rss_handler, cover_letter
from dotenv import load_dotenv

load_dotenv(".env")
bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    raise ValueError("Bot token not found. Please check your .env file.")

async def error(update, context):
    print(f'Update {update} caused error {context.error}')

def main():
    app = Application.builder().token(bot_token).build()

    app.add_handler(CommandHandler('start', rss_handler.start_command))
    app.add_handler(CommandHandler('stop', rss_handler.stop_command))
    app.add_handler(CommandHandler('check_url', rss_handler.check_url_command))
    app.add_handler(CommandHandler('create_cover_letter', cover_letter.create_cover_letter))

    app.add_handler(MessageHandler(filters.TEXT, rss_handler.handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
