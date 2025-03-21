from telegram import Update
from telegram.ext import ContextTypes
from utils.scraper import scrape_content
from services.ai_service import generate_cover_letter

async def create_cover_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text.split(" ")[1]
        await update.message.reply_text("Scraping content...")

        text_content = scrape_content(url)

        await update.message.reply_text("Generating cover letter...")

        cover_letter = generate_cover_letter(text_content)
        await update.message.reply_text(cover_letter)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        print(f"Cover letter error: {e}")
