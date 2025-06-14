from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Вставь сюда свой токен от BotFather
TOKEN = '8030938683:AAGiYEOw9ZiYc7bZLwXc-5Kl1pSFL7YIZJM'

# Клавиатура с двумя кнопками
keyboard = [['Source Barrier', 'North Barrier']]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Выбери одну из опций:',
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == 'Source Barrier':
        await update.message.reply_text('Ты выбрал: Source Barrier ✅')
    elif text == 'North Barrier':
        await update.message.reply_text('Ты выбрал: North Barrier ✅')
    else:
        await update.message.reply_text('Пожалуйста, выбери кнопку из меню.')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
