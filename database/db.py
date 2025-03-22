from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("Supabase url not found. Please check your .env file.")
elif not SUPABASE_KEY:
    raise ValueError("Supabase key not found. Please check your .env file.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def add_chat_id(chat_id):
    supabase.table('subscribers').insert({"chat_id": str(chat_id)}).execute()

async def remove_chat_id(chat_id):
    supabase.table('subscribers').delete().eq('chat_id', str(chat_id)).execute()

async def get_all_chat_ids():
    data = supabase.table('subscribers').select("chat_id").execute()
    return [entry['chat_id'] for entry in data.data]
