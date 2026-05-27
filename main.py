import logging
from bot.telegram_bot import run_bot
from config.settings import configure_logging

def main():
    configure_logging()
    logging.info("Запуск AI Model Advisor System")
    run_bot()

if __name__ == "__main__":
    main()