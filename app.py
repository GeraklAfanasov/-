from flask import Flask, request, jsonify
from collections import Counter
import re
import os
import logging

app = Flask(__name__)
app.json.ensure_ascii = False  # Отключаем экранирование ASCII для корректного отображения кириллицы

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.INFO)

def count_words(text):
    """Подсчитывает количество слов в тексте (исключая пунктуацию)."""
    words = re.findall(r'\w+', text.lower())
    return len(words)

def get_most_frequent_words(text, top_n=10):
    """Возвращает топ-N самых частотных слов."""
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """
    POST /analyze
    Принимает JSON: {"text": "строка"}
    Возвращает JSON: {"server_port": "...", "word_count": int, "most_frequent_words": [...]}
    """
    current_port = os.environ.get('PORT', '5000')
    print(f"!!! ЗАПРОС ОБРАБОТАН НА ПОРТУ {current_port} !!!")

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data['text']
    if not isinstance(text, str):
        return jsonify({"error": "'text' must be a string"}), 400
    
    result = {
        "server_port": current_port,
        "word_count": count_words(text),
        "most_frequent_words": [
            {"word": w, "count": c} for w, c in get_most_frequent_words(text)
        ]
    }
    
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"--> Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False) # nosec B104