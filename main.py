from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

# 🛡 Безопасно загружаем токен из переменной окружения
# TOKEN = os.getenv("BOT_TOKEN")

TOKEN2 = '8030938683:AAGiYEOw9ZiYc7bZLwXc-5Kl1pSFL7YIZJM'

# 🔗 URL для каждого шлагбаума
URL_SOURCE = 'https://api.pushcut.io/2ztWwEmVX4f8IlE1pTohY/notifications/Barrier%20Source'
URL_NORTH = 'https://api.pushcut.io/2ztWwEmVX4f8IlE1pTohY/notifications/Barrier%20North'

# 📱 Клавиатура с кнопками
keyboard = [['Source Barrier', 'North Barrier']]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

# 👋 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Выбери шлагбаум:',
        reply_markup=reply_markup
    )

# 📦 Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == 'Source Barrier':
        await send_pushcut_request(update, URL_SOURCE, 'Source Barrier')
    elif text == 'North Barrier':
        await send_pushcut_request(update, URL_NORTH, 'North Barrier')
    else:
        await update.message.reply_text('Пожалуйста, выбери кнопку из меню.')

# 🚪 Отправка Pushcut-запроса
async def send_pushcut_request(update: Update, url: str, name: str):
    try:
        response = requests.post(url)
        if response.status_code == 200:
            await update.message.reply_text(f'🟢 {name} открыт ✅')
        else:
            await update.message.reply_text(f'⚠️ {name} — ошибка: {response.status_code}')
    except Exception as e:
        await update.message.reply_text(f'❌ {name} — ошибка при запросе: {e}')

# 🚀 Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN2).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
