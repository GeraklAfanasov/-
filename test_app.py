import unittest
from app import app, count_words, get_most_frequent_words

class TestTextAnalysis(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_logic_functions(self):
        """Тестирование функций подсчета и частотности"""
        text = "Test text. Test!"
        self.assertEqual(count_words(text), 3)
        
        freq = get_most_frequent_words(text, top_n=1)
        self.assertEqual(freq[0][0], "test")
        self.assertEqual(freq[0][1], 2)
    
    def test_analyze_endpoint(self):
        """Тестирование полного цикла API."""
        response = self.client.post(
            '/analyze',
            json={"text": "hello world hello"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('server_port', data)
        self.assertEqual(data['word_count'], 3)
        self.assertEqual(data['most_frequent_words'][0]['word'], 'hello')

    def test_errors(self):
        """Тестирование обработки ошибок."""
        # Нет JSON
        resp = self.client.post('/analyze', data="error")
        self.assertEqual(resp.status_code, 400)
        
        # Нет поля text
        resp = self.client.post('/analyze', json={})
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()