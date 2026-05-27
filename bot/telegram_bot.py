import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.settings import TELEGRAM_BOT_TOKEN
from backend.classifier import classify_task
from backend.rating import calculate_rating
from backend.recommender import build_recommendation

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я помогу подобрать ИИ-модель под твою задачу.\n\n"
        "Просто опиши, что нужно сделать, например:\n"
        "• «Исправить ошибку в Python-коде»\n"
        "• «Перевести статью с английского»\n"
        "• «Решить дифференциальное уравнение»\n"
        "• «Сгенерировать SEO-текст для сайта»"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    logger.info(f"Получено сообщение от {update.effective_user.username}: {user_message}")

    if not user_message:
        await update.message.reply_text("⚠️ Пожалуйста, введите текст задачи.")
        return

    await update.message.chat.send_action("typing")

    try:
        # 1. Классификация
        category = classify_task(user_message)

        # 2. Расчет рейтинга
        rated = calculate_rating(category)

        # 3. Формирование ответа
        response = build_recommendation(category, rated)

        await update.message.reply_html(response)
        logger.info(f"Рекомендация отправлена пользователю {update.effective_user.username}")

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке запроса.\n"
            "Проверьте, запущен ли сервер Ollama, и попробуйте снова."
        )

def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Telegram-бот запущен")
    app.run_polling()