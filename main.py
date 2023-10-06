import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token API bot Telegram Anda
TOKEN = '6356132155:AAGuHxZ97zxaPxfW4MwiF-iqfSOlaEsTiW4'

# Membuat objek Updater dan Dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Fungsi untuk mengunduh video dari YouTube
def download_video(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    # Periksa apakah pesan pengguna mengandung tautan YouTube
    if text and text.startswith('https://www.youtube.com/'):
        try:
            # Mendapatkan tautan video dari pesan pengguna
            video_url = text

            # Mengunduh video menggunakan pytube
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            video_file = stream.download()

            # Mengirim video ke pengguna
            update.message.reply_video(video=open(video_file, 'rb'))

        except Exception as e:
            update.message.reply_text(f'Gagal mengunduh video: {str(e)}')
    else:
        update.message.reply_text('Kirimkan tautan video YouTube yang valid.')

# Menambahkan handler perintah /download
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

# Menjalankan bot
updater.start_polling()
updater.idle()
  
