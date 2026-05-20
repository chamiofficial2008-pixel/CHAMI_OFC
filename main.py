import yt_dlp
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ['BOT_TOKEN']

# Hosting walata keep alive
app = Flask('')

@app.route('/')
def home():
    return "Bot eka wada!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def download(update, context):
    url = update.message.text
    msg = await update.message.reply_text("Download wenawa...⏳")
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            
        await context.bot.send_video(update.effective_chat.id, open(filepath, 'rb'))
        os.remove(filepath)
        await msg.delete()
        
    except Exception as e:
        await msg.edit_text(f"Error ekak awa: {str(e)}")

def main():
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("Bot eka start una!")
    application.run_polling()

if __name__ == '__main__':
    main()
