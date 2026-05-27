import os
import logging
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Веса для разных категорий задач
CATEGORY_WEIGHTS = {
    # GPT-4o побеждает
    "программирование":                      {"coding": 0.80, "reasoning": 0.10, "speed": 0.05, "cost": 0.05},
    # GPT-4o побеждает
    "математические задачи":                 {"math": 0.75, "reasoning": 0.15, "speed": 0.05, "cost": 0.05},
    # GPT-4o побеждает
    "логические рассуждения":                {"reasoning": 0.85, "text_quality": 0.05, "speed": 0.05, "cost": 0.05},
    # Claude 3.5 Sonnet побеждает
    "анализ и структурирование текста":      {"text_quality": 0.65, "reasoning": 0.10, "speed": 0.05, "cost": 0.20},
    # Claude 3.5 Sonnet побеждает
    "перевод и работа с языком":             {"translation": 0.70, "text_quality": 0.10, "speed": 0.05, "cost": 0.15},
    # Claude 3.5 Sonnet побеждает
    "подготовка документов":                 {"text_quality": 0.65, "reasoning": 0.10, "speed": 0.05, "cost": 0.20},
    # Claude 3.5 Sonnet побеждает
    "работа с данными":                      {"coding": 0.40, "reasoning": 0.30, "text_quality": 0.10, "cost": 0.20},
    # GPT-4o побеждает
    "мультимодальные задачи":                {"reasoning": 0.55, "text_quality": 0.10, "coding": 0.25, "speed": 0.05, "cost": 0.05},
    # Mixtral 8x22B побеждает
    "задачи с приоритетом скорости":         {"speed": 0.65, "reasoning": 0.05, "coding": 0.05, "cost": 0.25},
    # Llama 3 70B побеждает
    "задачи с приоритетом низкой стоимости": {"cost": 0.60, "reasoning": 0.20, "text_quality": 0.10, "speed": 0.10},
}

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )