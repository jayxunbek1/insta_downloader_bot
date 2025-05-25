import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from instaloader import Instaloader, Post

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply("Instagram link yuboring (post, video, rasm).")

@bot.on_message(filters.text & ~filters.command("start"))
async def download_instagram(client, message: Message):
    url = message.text.strip()
    if "instagram.com" not in url:
        await message.reply("Instagram link yuboring.")
        return
    await message.reply("Yuklanmoqda...")

    loader = Instaloader()
    try:
        shortcode = url.strip("/").split("/")[-1]
        post = Post.from_shortcode(loader.context, shortcode)
        file_path = f"{shortcode}.mp4" if post.is_video else f"{shortcode}.jpg"
        loader.download_post(post, target=shortcode)
        for file in os.listdir():
            if file.endswith(".mp4") or file.endswith(".jpg"):
                await client.send_document(message.chat.id, file)
                os.remove(file)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

bot.run()
