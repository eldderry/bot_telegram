import logging

logger = logging.getLogger(__name__)

# Метки категорий
CATEGORY_METRIC_LABELS = {
    "программирование":                      ("качестве выполнения задач программирования (HumanEval)", "coding"),
    "математические задачи":                 ("качестве решения математических задач (MATH)", "math"),
    "логические рассуждения":                ("качестве рассуждений (ARC)", "reasoning"),
    "анализ и структурирование текста":      ("качестве работы с текстом (MT-Bench)", "text_quality"),
    "перевод и работа с языком":             ("качестве перевода (BLEU)", "translation"),
    "подготовка документов":                 ("качестве работы с текстом (MT-Bench)", "text_quality"),
    "работа с данными":                      ("качестве анализа данных и кодинге", "coding"),
    "мультимодальные задачи":                ("мультимодальных возможностях", "reasoning"),
    "задачи с приоритетом скорости":         ("скорости ответа", "reasoning"),
    "задачи с приоритетом низкой стоимости": ("стоимости использования", "reasoning"),
}

# Показатели для сравнения моделей
METRIC_LABELS = {
    "coding":       "💻 Качество программирования",
    "math":         "📐 Качество математики",
    "reasoning":    "🧠 Качество рассуждений",
    "text_quality": "📝 Качество работы с текстом",
    "translation":  "🌐 Перевод и работа с языком",
}


def _stars(score: int) -> str:
    filled = round(score / 20)
    return "⭐" * filled + "☆" * (5 - filled)


def _bar(score: int, width: int = 10) -> str:
    filled = round(score / 100 * width)
    return "█" * filled + "░" * (width - filled)


def _medal(rank: int) -> str:
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    return medals.get(rank, f"{rank}.")


def build_recommendation(category: str, rated_models: list) -> str:
    if not rated_models:
        return (
            "🤔 Не удалось точно определить тип задачи.\n"
            "Пожалуйста, опишите задачу подробнее.\n"
            "Например: «Нужно написать функцию сортировки на Python»"
        )

    best = rated_models[0]
    alternatives = rated_models[1:]

    metric_label, key_metric = CATEGORY_METRIC_LABELS.get(
        category, ("комплексных тестах", "reasoning")
    )

    # Заголовок
    message = (
        f"🎯 <b>Категория задачи:</b> {category.capitalize()}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    # Лучшая модель
    message += (
        f"🥇 <b>Рекомендуемая модель: {best['name']}</b>\n"
        f"🏢 Провайдер: {best['provider']}\n"
        f"⭐ Рейтинг для задачи: {best['rating']:.1f} / 100\n\n"
        f"📖 <b>Описание:</b>\n{best.get('description', '—')}\n\n"
    )

    # Показатели модели
    message += "📊 <b>Показатели модели:</b>\n"
    for metric_key, metric_name in METRIC_LABELS.items():
        val = best.get(metric_key, 0)
        message += f"  {metric_name}: {_bar(val)} {val}/100\n"

    # Возможность работы с изображениями или файлами
    multimodal_str = "✅ Поддерживается" if best.get("multimodal") else "❌ Не поддерживается"
    message += f"  🖼️ Работа с изображениями/файлами: {multimodal_str}\n"
    # Скорость ответа
    message += f"  ⚡ Скорость ответа: {best['speed_ms']} мс\n"
    # Стоимость использования
    message += f"  💰 Стоимость использования: ${best['cost_per_1k']}/1K токенов\n"
    # Ограничения модели
    if best.get("limitations"):
        message += f"\n⚠️ <b>Ограничения модели:</b>\n  {best['limitations']}\n"

    # Сильные стороны
    if best.get("strengths"):
        message += "\n✅ <b>Сильные стороны:</b>\n"
        for s in best["strengths"]:
            message += f"  • {s}\n"

    # Причина выбора
    message += "\n<b>Причина выбора:</b>\n"
    if category == "задачи с приоритетом скорости":
        message += (
            f"Задача требует максимально быстрого ответа. "
            f"Модель отвечает за <b>{best['speed_ms']} мс</b> — "
            f"быстрее большинства конкурентов. "
            f"Стоимость: ${best['cost_per_1k']}/1K токенов.\n"
        )
    elif category == "задачи с приоритетом низкой стоимости":
        message += (
            f"Задача требует минимальных затрат. "
            f"Стоимость: <b>${best['cost_per_1k']}/1K токенов</b> — "
            f"одна из самых низких. Скорость ответа: {best['speed_ms']} мс.\n"
        )
    elif category == "мультимодальные задачи":
        message += (
            f"Задача требует работы с изображениями или файлами. "
            f"Модель поддерживает мультимодальный ввод и показывает "
            f"высокие результаты в {metric_label}.\n"
        )
    else:
        message += (
            f"Задача относится к категории «{category}». "
            f"Модель показывает лучшие результаты в {metric_label} "
            f"({best.get(key_metric, 0)}/100) при оптимальном соотношении "
            f"скорости (~{best['speed_ms']} мс) и стоимости "
            f"(${best['cost_per_1k']}/1K токенов).\n"
        )

    # Сравнение всех моделей
    message += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    message += "📈 <b>Сравнение всех моделей:</b>\n\n"

    for rank, model in enumerate(rated_models, 1):
        medal = _medal(rank)
        bar = _bar(int(min(model["rating"], 100)))
        mm = "🖼️✅" if model.get("multimodal") else "🖼️❌"
        message += (
            f"{medal} <b>{model['name']}</b> ({model['provider']})\n"
            f"   Рейтинг: {bar} {model['rating']:.1f}\n"
            f"   {_stars(model.get(key_metric, 0))}  "
            f"{METRIC_LABELS.get(key_metric, 'Показатель')}: {model.get(key_metric, 0)}/100 | "
            f"⚡{model['speed_ms']}мс | 💰${model['cost_per_1k']}/1K | {mm}\n\n"
        )

    # Альтернативы
    if alternatives:
        message += "━━━━━━━━━━━━━━━━━━━━━━\n"
        message += "🔀 <b>Альтернативы:</b>\n\n"
        for i, alt in enumerate(alternatives[:3], 1):
            if alt["speed_ms"] < best["speed_ms"] and alt["cost_per_1k"] <= best["cost_per_1k"]:
                advantage = "⚡ Быстрее и дешевле"
            elif alt["speed_ms"] < best["speed_ms"]:
                advantage = "⚡ Быстрее"
            elif alt["cost_per_1k"] < best["cost_per_1k"]:
                advantage = "💰 Экономичнее"
            else:
                advantage = "⚖️ Другой баланс метрик"

            message += (
                f"{i}. <b>{alt['name']}</b> — {advantage}\n"
                f"   {alt.get('description', '').split('.')[0]}.\n"
                f"   Лучше всего: {alt.get('best_for', '—')}\n\n"
            )

    message += (
        "\n<i>ℹ️ Рекомендация основана на данных бенчмарков (HumanEval, MATH, "
        "MT-Bench, ARC, BLEU) и весовых коэффициентах категории задачи.</i>"
    )

    return message