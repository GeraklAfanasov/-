from flask import Flask, request, jsonify
from collections import Counter
import re

app = Flask(__name__)


def count_words(text):
    """
    Подсчитывает общее количество слов в тексте.
    
    Args:
        text (str): Входной текст для анализа
        
    Returns:
        int: Количество слов в тексте
    """
    # Разбиваем текст на слова, используя регулярное выражение
    # \w+ соответствует одному или более буквенно-цифровым символам
    words = re.findall(r'\w+', text.lower())
    return len(words)


def get_most_frequent_words(text, top_n=10):
    """
    Определяет самые частотные слова в тексте.
    
    Args:
        text (str): Входной текст для анализа
        top_n (int): Количество наиболее частотных слов для возврата (по умолчанию 10)
        
    Returns:
        list: Список кортежей (слово, частота) для топ-N слов
    """
    # Разбиваем текст на слова и приводим к нижнему регистру
    words = re.findall(r'\w+', text.lower())
    # Используем Counter для подсчета частоты каждого слова
    word_counts = Counter(words)
    # Возвращаем топ-N наиболее частотных слов
    return word_counts.most_common(top_n)


@app.route('/analyze', methods=['POST'])
def analyze_text():
    """
    RESTful API endpoint для анализа текста.
    
    Принимает POST запрос с JSON телом вида: {"text": "ваш текст"}
    Возвращает JSON с количеством слов и топ наиболее частотных слов.
    
    Returns:
        JSON: {
            "word_count": int,
            "most_frequent_words": [{"word": str, "count": int}, ...]
        }
    """
    # Проверяем, что запрос содержит JSON данные
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    # Получаем JSON данные из запроса
    data = request.get_json()
    
    # Проверяем наличие поля "text" в запросе
    if 'text' not in data:
        return jsonify({"error": "Missing 'text' field in request"}), 400
    
    # Получаем текст из запроса
    text = data['text']
    
    # Проверяем, что текст является строкой
    if not isinstance(text, str):
        return jsonify({"error": "'text' must be a string"}), 400
    
    # Подсчитываем количество слов
    word_count = count_words(text)
    
    # Получаем топ наиболее частотных слов
    frequent_words = get_most_frequent_words(text)
    
    # Формируем ответ в формате JSON
    # Преобразуем список кортежей в список словарей для удобства
    result = {
        "word_count": word_count,
        "most_frequent_words": [
            {"word": word, "count": count} 
            for word, count in frequent_words
        ]
    }
    
    return jsonify(result), 200


if __name__ == '__main__':
    # Запускаем Flask приложение
    # host='0.0.0.0' позволяет принимать запросы извне
    # port берется из переменной окружения или используется 5000 по умолчанию
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
