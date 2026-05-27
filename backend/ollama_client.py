import requests
import logging
from config.settings import OLLAMA_API_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)

def analyze_task(prompt: str) -> str:
    url = f"{OLLAMA_API_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "max_tokens": 20
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        logger.info(f"Ответ Ollama получен: {result[:100]}...")
        return result
    except requests.exceptions.Timeout:
        logger.error("Таймаут Ollama API")
        raise Exception("Сервис анализа временно недоступен (таймаут)")
    except requests.exceptions.ConnectionError:
        logger.error("Ollama API недоступен")
        raise Exception("Сервис анализа недоступен (ошибка подключения)")
    except Exception as e:
        logger.error(f"Ошибка Ollama API: {e}")
        raise