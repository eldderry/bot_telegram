import logging
from config.settings import CATEGORY_WEIGHTS
from data.models_db import MODELS

logger = logging.getLogger(__name__)

# Метрики, которые участвуют в расчёте рейтинга
QUALITY_METRICS = ["coding", "math", "reasoning", "text_quality", "translation"]


def calculate_rating(category: str) -> list:
    weights = CATEGORY_WEIGHTS.get(category, CATEGORY_WEIGHTS["логические рассуждения"])

    # Для мультимодальных задач - исключаем модели без поддержки
    require_multimodal = category == "мультимодальные задачи"

    rated_models = []
    for model in MODELS:
        # Пропускаем немультимодальные модели для мультимодальных задач
        if require_multimodal and not model.get("multimodal", False):
            continue

        score = 0.0

        # Качественные метрики
        for metric in QUALITY_METRICS:
            if metric in weights:
                score += model.get(metric, 0) * weights[metric]

        #Стоимость
        cost_penalty = model["cost_per_1k"] * 1000 * weights.get("cost", 0)
        score -= cost_penalty

        # Бонус за скорость
        speed_bonus = (1000 - model["speed_ms"]) / 100 * weights.get("speed", 0)
        score += speed_bonus

        rated_models.append({
            **model,
            "rating": round(score, 2),
            "cost_penalty": round(cost_penalty, 2),
            "speed_bonus": round(speed_bonus, 2),
        })

    if not rated_models:
        # Если фильтр убрал все модели - возвращаем все без фильтра
        logger.warning(f"Фильтр убрал все модели для '{category}', возвращаем все модели")
        return calculate_rating("логика")

    rated_models.sort(key=lambda x: x["rating"], reverse=True)
    logger.info(
        f"Рейтинг для '{category}': "
        + " | ".join(f"{m['name']} {m['rating']}" for m in rated_models)
    )
    return rated_models