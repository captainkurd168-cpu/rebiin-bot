import os
import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
import yt_dlp
from flask import Flask
from threading import Thread

# ---------------------------------------------
# 1. Config (ڕێکخستنەکان)
# ---------------------------------------------
TOKEN = os.getenv("BOT_TOKEN") # توکن لە Render وەردەگرێت

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------------------------------------
# 2. Flask Server (بۆ ئەوەی Render نەخەوێت)
# ---------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "🦁 Lion Rebin Bot is Alive!", 200

def run_http():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# ---------------------------------------------
# 3. پەیامەکان (بادینی + ئیمۆجی ✨)
# ---------------------------------------------
wait_messages = [
    "⏳ بۆستە برا، رێبین گۆتیە ب کوالێتیەکا باش بینە... 🫡",
    "🏃‍♂️ خەما تە نەبیت، ئەز و رێبین یێ خەریکی ڤیدیۆیا تەینە... 🔥",
    "☕ چایەکێ ل سەر حسابا رێبین ڤەخۆ هەتا دهێت... 🍵✨",
    "🧐 سەکینە، ئەز ل سەر سێرڤەرێ رێبین یێ دگەرم... 🚀",
    "⚡ ب فەرمانا رێبین، دێ نوکە وەک بریسیێ ئینم! ✨🦁",
    "🔧 تۆزەکێ بێهنا خۆ فراە بکە، رێبین دبێژیت: تشتێ باش سەبرێ دڤێت... 💎"
]

success_messages = [
    "✅ فەرموو، ئەڤە ژی دیاری یە ژ لایێ (رێبین) ڤە... 🎁✨",
    "🫡 کەرەم کە، رێبین سلاڤا ل تە دکەت و دبێژیت: نۆشی گیان... ✨🌹",
    "🎁 ئەڤە ژی ئەو ڤیدیۆیا تە دڤیا، ب خاترا رێبین هات... ⭐👑",
    "🔥 وەڵاهی ڤیدیۆیەکا جوانە، زەوقێ تە و رێبین یێ لێک نێزیکە! ✨🤴",
    "👑 فەرموو ئەڤە ژی داخوازیا تە، خزمەتکارێ رێبین یێ حازرە... 🫡💎",
    "📱 تمام بوو! رێبین گۆت: ئێکسەر بۆ بفرێکە... 🚀🔥"
]

error_messages = [
    "❌ وەی بابۆ! ئەز هاتمە گرتن... رێبین دێ ژ من تۆڕە بیت! 🤦‍♂️💔",
    "🤕 ببورە، رێبین گەلەک هەوڵدا بەس نەهات... لینک خەلەتە 🚫",
    "🔒 ئەڤە قفلە برا، رێبین ژی نەشێت بچیتە ژوور... 🗝️⚠️",
    "😵 سێرڤەر وەستیا... هەوارا خۆ ببەنە بەر رێبین! 🆘📢"
]

hello_messages = [
    "👋 ئۆوو بەخێر هاتی! ئەز بۆتێ (رێبین)ـم، چ خزمەت هەیە؟ ✨🦁",
    "🌹 سلاڤ ل تە! رێبین راسپاردیمە کو کارێ تە ب رێڤە ببەم... 🫡✨",
    "🤖 ئەز رۆبۆتێ رێبینـم، لینکێ بدە من و تە کار نەبیت! ⚡💎",
    "⚡ سێرڤەرێ رێبین یێ ئامادەیە! تەنێ لینکی بینە... 🔥👑"
]

# ---------------------------------------------
# 4. فەنکشنی داونلۆد (Instagram & TikTok)
# ---------------------------------------------
def download_video(url):
    timestamp = int(time.time())
    filename = f"video_{timestamp}.mp4"
    
    ydl_opts = {
        'format': 'best', # باشترین کوالێتی
        'outtmpl': filename,
        'max_filesize': 50 * 1024 * 1024, # دیاریکردنی 50 مێگابایت وەک لیمیت
        'noplaylist': True,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return filename
    except Exception as e:
        print(f"Download Error: {e}")
        return None

# ---------------------------------------------
# 5. Handlers (وەرگرتنی فەرمانەکان)
# ---------------------------------------------
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    txt = random.choice(hello_messages)
    await message.answer(txt)

@dp.message()
async def message_handler(message: types.Message):
    url = message.text
    
    # تەنێ TikTok و Instagram وەردەگرێت
    if "tiktok.com" in url or "instagram.com" in url:
        wait_msg = random.choice(wait_messages)
        status_msg = await message.answer(wait_msg)
        
        # دەستپێکردنی داونلۆد
        file_path = download_video(url)
        
        if file_path and os.path.exists(file_path):
            try:
                caption_msg = random.choice(success_messages)
                final_caption = f"{caption_msg}\n\n🤖 *Downloaded by Rebin's Bot* ✨"
                
                video_file = FSInputFile(file_path)
                await message.answer_video(
                    video_file, 
                    caption=final_caption, 
                    parse_mode="Markdown"
                )
                
                # سڕینەوەی فایل دوای ناردن
                os.remove(file_path)
            except Exception as e:
                await message.answer(f"❌ کێشەیەک هەیە: {e}")
            finally:
                # سڕینەوەی پەیامی 'بۆستە...'
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
                except:
                    pass
        else:
            err_txt = random.choice(error_messages)
            await message.answer(err_txt)
    else:
        # ئەگەر لینکەکە تیکتۆک یان ئینستا نەبوو
        await message.answer("ئەڤە چیە برا؟ تەنێ لینکێ **TikTok** یان **Instagram** بفرێکە! 😒📱")

# ---------------------------------------------
# 6. Main Execution
# ---------------------------------------------
async def main():
    print("🦁 Lion Rebin Bot is starting...")
    keep_alive() # سێرڤەرەکە پێ دەکات
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
