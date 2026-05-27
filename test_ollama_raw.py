import requests

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3.2:1b",
    "prompt": "Скажи одно слово: программирование",
    "stream": False
}

print(f"Отправка запроса к {url} с моделью {payload['model']}...")

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text[:500]}")
except Exception as e:
    print(f"Ошибка: {e}")