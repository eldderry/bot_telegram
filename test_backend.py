from backend.ollama_client import analyze_task
from backend.classifier import classify_task

# Тест 1: Проверка связи с Ollama
print("=== Тест Ollama API ===")
try:
    result = analyze_task("Скажи: программирование")
    print(f"Ответ Ollama: {result}")
except Exception as e:
    print(f"Ошибка: {e}")

# Тест 2: Проверка классификации
print("\n=== Тест классификации ===")
category = classify_task("Исправить ошибку в Python коде")
print(f"Категория: {category}")

# Тест 3: Проверка рейтинга
print("\n=== Тест рейтинга ===")
from backend.rating import calculate_rating
rated = calculate_rating(category)
for m in rated[:3]:
    print(f"{m['name']}: {m['rating']}")

# Тест 4: Проверка рекомендации
print("\n=== Тест рекомендации ===")
from backend.recommender import build_recommendation
msg = build_recommendation(category, rated)
print(msg)