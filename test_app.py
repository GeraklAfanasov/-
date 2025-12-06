import unittest
from app import app, count_words, get_most_frequent_words


class TestTextAnalysis(unittest.TestCase):
    """
    Класс для unit-тестирования функциональности анализа текста.
    Наследуется от unittest.TestCase для использования методов тестирования.
    """
    
    def setUp(self):
        """
        Метод setUp вызывается перед каждым тестом.
        Создает тестовый клиент Flask для выполнения HTTP запросов.
        """
        # Создаем тестовый клиент Flask приложения
        self.client = app.test_client()
        # Устанавливаем режим тестирования
        app.config['TESTING'] = True
    
    def test_count_words_basic(self):
        """
        Тест для проверки подсчета слов в простом тексте.
        """
        # Простой текст с известным количеством слов
        text = "Hello world this is a test"
        # Ожидаем 6 слов
        self.assertEqual(count_words(text), 6)
    
    def test_count_words_empty(self):
        """
        Тест для проверки подсчета слов в пустом тексте.
        """
        # Пустой текст должен возвращать 0 слов
        self.assertEqual(count_words(""), 0)
    
    def test_count_words_with_punctuation(self):
        """
        Тест для проверки подсчета слов с пунктуацией.
        """
        # Текст с пунктуацией - слова должны быть правильно подсчитаны
        text = "Hello, world! How are you?"
        # Ожидаем 5 слов (hello, world, how, are, you)
        self.assertEqual(count_words(text), 5)
    
    def test_get_most_frequent_words(self):
        """
        Тест для проверки определения наиболее частотных слов.
        """
        # Текст, где "test" встречается 3 раза, "word" - 2 раза
        text = "test test test word word"
        # Получаем топ-2 слова
        result = get_most_frequent_words(text, top_n=2)
        # Проверяем, что "test" на первом месте с частотой 3
        self.assertEqual(result[0][0], "test")
        self.assertEqual(result[0][1], 3)
        # Проверяем, что "word" на втором месте с частотой 2
        self.assertEqual(result[1][0], "word")
        self.assertEqual(result[1][1], 2)
    
    def test_analyze_endpoint_success(self):
        """
        Тест для проверки успешного выполнения POST /analyze endpoint.
        """
        # Отправляем POST запрос с валидными данными
        response = self.client.post(
            '/analyze',
            json={"text": "hello world hello"},
            content_type='application/json'
        )
        # Проверяем, что статус код 200 (успех)
        self.assertEqual(response.status_code, 200)
        # Получаем JSON данные из ответа
        data = response.get_json()
        # Проверяем наличие поля word_count
        self.assertIn('word_count', data)
        # Проверяем наличие поля most_frequent_words
        self.assertIn('most_frequent_words', data)
        # Проверяем, что количество слов равно 3
        self.assertEqual(data['word_count'], 3)
        # Проверяем, что "hello" является наиболее частотным словом
        self.assertEqual(data['most_frequent_words'][0]['word'], 'hello')
        self.assertEqual(data['most_frequent_words'][0]['count'], 2)
    
    def test_analyze_endpoint_missing_text(self):
        """
        Тест для проверки обработки ошибки при отсутствии поля "text".
        """
        # Отправляем POST запрос без поля "text"
        response = self.client.post(
            '/analyze',
            json={},
            content_type='application/json'
        )
        # Проверяем, что статус код 400 (ошибка клиента)
        self.assertEqual(response.status_code, 400)
        # Проверяем наличие сообщения об ошибке
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_analyze_endpoint_not_json(self):
        """
        Тест для проверки обработки ошибки при отправке не-JSON данных.
        """
        # Отправляем POST запрос с обычными данными (не JSON)
        response = self.client.post(
            '/analyze',
            data="not json",
            content_type='text/plain'
        )
        # Проверяем, что статус код 400 (ошибка клиента)
        self.assertEqual(response.status_code, 400)
    
    def test_analyze_endpoint_invalid_text_type(self):
        """
        Тест для проверки обработки ошибки при неверном типе поля "text".
        """
        # Отправляем POST запрос, где "text" не является строкой
        response = self.client.post(
            '/analyze',
            json={"text": 123},
            content_type='application/json'
        )
        # Проверяем, что статус код 400 (ошибка клиента)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    # Запускаем все тесты
    unittest.main()
