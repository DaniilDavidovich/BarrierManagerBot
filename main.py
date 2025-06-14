from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import asyncio
import os

# 🔐 Токен (замени на переменную окружения при деплое)
TOKEN = '8030938683:AAGiYEOw9ZiYc7bZLwXc-5Kl1pSFL7YIZJM'

# 🔗 Ссылки на шлагбаумы
URL_SOURCE = 'https://api.pushcut.io/2ztWwEmVX4f8IlE1pTohY/notifications/Barrier%20Source'
URL_NORTH = 'https://api.pushcut.io/2ztWwEmVX4f8IlE1pTohY/notifications/Barrier%20North'

# 📱 Клавиатура
keyboard = [['Source Barrier', 'North Barrier']]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

# 🔒 Флаг активности
is_busy = False

# 🚀 Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Выбери шлагбаум:',
        reply_markup=reply_markup
    )

# 🔁 Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_busy

    if is_busy:
        await update.message.reply_text("⏳ Уже выполняется операция, подожди пару секунд...")
        return

    text = update.message.text

    if text == 'Source Barrier':
        asyncio.create_task(wrapped_request(update, URL_SOURCE, 'Source Barrier'))
    elif text == 'North Barrier':
        asyncio.create_task(wrapped_request(update, URL_NORTH, 'North Barrier'))
    else:
        await update.message.reply_text("Пожалуйста, выбери кнопку из меню.")

# 🧠 Обёртка с установкой и сбросом флага
async def wrapped_request(update: Update, url: str, name: str):
    global is_busy
    is_busy = True
    try:
        await send_pushcut_request(update, url, name)
    finally:
        is_busy = False

# 📤 Запрос + 5 сообщений
async def send_pushcut_request(update: Update, url: str, name: str):
    for i in range(5):
        try:
            response = requests.post(url)
            if response.status_code == 200:
                await update.message.reply_text(f'🟢 {name}: уведомление номер ({i+1}/5) отправлено')
            else:
                await update.message.reply_text(f'⚠️ {name} — ошибка: {response.status_code} ({i+1}/5)')
        except Exception as e:
            await update.message.reply_text(f'❌ {name} — ошибка при запросе: {e} ({i+1}/5)')

        if i < 4:
            await asyncio.sleep(2)

# 🏁 Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
