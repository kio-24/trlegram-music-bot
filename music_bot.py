import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yt_dlp
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

music_queue = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = f"မင်္ဂလာပါ {user.first_name}!\n\n"
    msg += "/play [link] - သီချင်းဖွင့်မယ်\n"
    msg += "/queue - တန်းစီစာရင်း"
    await update.message.reply_text(msg)

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Link လေးပို့ပေးပါ။")
        return
    
    msg = await update.message.reply_text("သီချင်းရှာနေပါတယ်...")
    
    try:
        url = context.args[0]
        ydl_opts = {'quiet': True, 'no_warnings': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            
            music_queue.append({
                'title': title,
                'url': url,
                'requested_by': update.effective_user.first_name
            })
            
            await msg.edit_text(f"✅ {title} ကို queue ထဲထည့်ပြီးပါပြီ။")
            
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")

async def queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not music_queue:
        await update.message.reply_text("Queue ထဲမှာဘာမှမရှိသေးပါဘူး။")
        return
    
    text = "Queue စာရင်း:\n"
    for i, song in enumerate(music_queue, 1):
        text += f"{i}. {song['title']}\n"
    
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("queue", queue))
    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()