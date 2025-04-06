>>> import telegram
from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading

# توکن ربات تلگرام که از BotFather گرفتی
TOKEN = "7243834241:AAHgRWMIQ6Y6DvWhFvkFMwEL4Kjehx7mr94"
# آی‌دی کانال تلگرام
CHANNEL_ID = "@Mim_PosterBot"

# لیستی برای ذخیره متن‌ها
messages = []
bot = telegram.Bot(token=TOKEN)

# تابع برای ارسال پیام به کانال
def send_message_to_channel(message):
    bot.send_message(chat_id=CHANNEL_ID, text=message)
    print(f"پیام ارسال شد: {message}")

# تابع برای اضافه کردن پیام توسط کاربر
def add_message(update, context):
    msg = update.message.text.replace('/add ', '')
    messages.append(msg)
    update.message.reply_text(f"متن '{msg}' به لیست اضافه شد!")

# تابع برای تنظیم زمان‌بندی و ارسال پیام‌ها
def schedule_messages():
    # مثلاً هر روز ساعت 8 صبح یه پیام ارسال کنه
    schedule.every().day.at("08:00").do(send_next_message)
    # یا هر 10 ثانیه یه پیام (برای تست)
    schedule.every(10).seconds.do(send_next_message)

def send_next_message():
    if messages:
        message = messages.pop(0)  # اولین پیام رو برمیداره و حذفش می‌کنه
        send_message_to_channel(message)
    else:
        print("هیچ پیامی برای ارسال نیست!")

# تابع برای اجرای زمان‌بندی در پس‌زمینه
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# راه‌اندازی ربات
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # دستور برای اضافه کردن پیام
    dp.add_handler(CommandHandler("add", add_message))

    # شروع ربات
    updater.start_polling()

    # اجرای زمان‌بندی در یه线程 جدا
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # تنظیم زمان‌بندی اولیه
    schedule_messages()

    updater.idle()

if __name__ == '__main__':
    main()
