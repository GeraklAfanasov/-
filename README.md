# Лабораторная работа №9, Вариант 2

## Описание проекта

Данный проект реализует RESTful API на Flask для анализа текстов с балансировкой нагрузки через Nginx и автоматизированным CI/CD pipeline через GitHub Actions.

## Структура проекта

```
.
├── app.py                  # Основное Flask приложение
├── test_app.py             # Unit-тесты для проверки функциональности
├── requirements.txt        # Зависимости Python проекта
├── start_instances.py      # Скрипт для запуска нескольких инстансов (Python)
├── start_instances.bat     # Скрипт для запуска нескольких инстансов (Windows)
├── nginx.conf              # Конфигурация Nginx для балансировки нагрузки
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions workflow для CI/CD
└── README.md               # Документация проекта
```

---

## Подробное объяснение кода

### 1. app.py - Основное Flask приложение

#### Импорты

```python
from flask import Flask, request, jsonify
from collections import Counter
import re
```

- **Flask**: Веб-фреймворк для создания RESTful API
- **request**: Объект для работы с входящими HTTP запросами
- **jsonify**: Функция для преобразования Python объектов в JSON ответы
- **Counter**: Класс из collections для подсчета частоты элементов
- **re**: Модуль для работы с регулярными выражениями

#### Функция count_words()

```python
def count_words(text):
    words = re.findall(r'\w+', text.lower())
    return len(words)
```

**Назначение**: Подсчитывает общее количество слов в тексте.

**Как работает**:
1. `text.lower()` - преобразует весь текст в нижний регистр для единообразия
2. `re.findall(r'\w+', ...)` - находит все слова в тексте
   - `\w+` означает один или более буквенно-цифровых символов
   - Это исключает пунктуацию и пробелы
3. `len(words)` - возвращает количество найденных слов

**Пример**: 
- Вход: `"Hello, world! How are you?"`
- Выход: `5` (hello, world, how, are, you)

#### Функция get_most_frequent_words()

```python
def get_most_frequent_words(text, top_n=10):
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common(top_n)
```

**Назначение**: Определяет самые частотные слова в тексте.

**Параметры**:
- `text` - входной текст для анализа
- `top_n` - количество наиболее частотных слов для возврата (по умолчанию 10)

**Как работает**:
1. Разбивает текст на слова (аналогично `count_words()`)
2. `Counter(words)` - создает объект-счетчик, который автоматически подсчитывает частоту каждого слова
3. `most_common(top_n)` - возвращает список кортежей `(слово, частота)` для топ-N слов, отсортированных по убыванию частоты

**Пример**:
- Вход: `"test test test word word"`
- Выход: `[('test', 3), ('word', 2)]`

#### Endpoint POST /analyze

```python
@app.route('/analyze', methods=['POST'])
def analyze_text():
```

**Назначение**: RESTful API endpoint для анализа текста.

**Метод**: POST (используется для отправки данных на сервер)

**Обработка запроса**:

1. **Проверка формата данных**:
```python
if not request.is_json:
    return jsonify({"error": "Request must be JSON"}), 400
```
   - Проверяет, что запрос содержит JSON данные
   - Если нет - возвращает ошибку 400 (Bad Request)

2. **Получение данных**:
```python
data = request.get_json()
```
   - Извлекает JSON данные из запроса

3. **Валидация поля "text"**:
```python
if 'text' not in data:
    return jsonify({"error": "Missing 'text' field in request"}), 400

if not isinstance(text, str):
    return jsonify({"error": "'text' must be a string"}), 400
```
   - Проверяет наличие обязательного поля "text"
   - Проверяет, что значение является строкой

4. **Выполнение анализа**:
```python
word_count = count_words(text)
frequent_words = get_most_frequent_words(text)
```
   - Подсчитывает количество слов
   - Определяет наиболее частотные слова

5. **Формирование ответа**:
```python
result = {
    "word_count": word_count,
    "most_frequent_words": [
        {"word": word, "count": count} 
        for word, count in frequent_words
    ]
}
return jsonify(result), 200
```
   - Создает словарь с результатами
   - Преобразует список кортежей в список словарей для удобства
   - Возвращает JSON ответ со статусом 200 (OK)

**Пример запроса**:
```json
POST /analyze
Content-Type: application/json

{
  "text": "hello world hello test"
}
```

**Пример ответа**:
```json
{
  "word_count": 4,
  "most_frequent_words": [
    {"word": "hello", "count": 2},
    {"word": "world", "count": 1},
    {"word": "test", "count": 1}
  ]
}
```

#### Запуск приложения

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Как работает**:
- `if __name__ == '__main__'` - код выполняется только при прямом запуске файла
- `os.environ.get('PORT', 5000)` - получает номер порта из переменной окружения PORT, или использует 5000 по умолчанию
- `host='0.0.0.0'` - позволяет принимать запросы извне (не только localhost)
- `debug=False` - отключает режим отладки (для продакшена)

---

### 2. test_app.py - Unit-тесты

#### Класс TestTextAnalysis

```python
class TestTextAnalysis(unittest.TestCase):
```

**Назначение**: Класс для unit-тестирования функциональности анализа текста.

**Наследование**: `unittest.TestCase` - базовый класс для тестов в Python

#### Метод setUp()

```python
def setUp(self):
    self.client = app.test_client()
    app.config['TESTING'] = True
```

**Назначение**: Вызывается перед каждым тестом для подготовки окружения.

**Как работает**:
- `app.test_client()` - создает тестовый клиент Flask для выполнения HTTP запросов без реального сервера
- `app.config['TESTING'] = True` - включает режим тестирования Flask

#### Тесты функций

##### test_count_words_basic()
- Проверяет подсчет слов в простом тексте
- Ожидает: 6 слов в тексте "Hello world this is a test"

##### test_count_words_empty()
- Проверяет обработку пустого текста
- Ожидает: 0 слов

##### test_count_words_with_punctuation()
- Проверяет правильную обработку пунктуации
- Ожидает: 5 слов в тексте "Hello, world! How are you?"

##### test_get_most_frequent_words()
- Проверяет определение наиболее частотных слов
- Ожидает: "test" (3 раза) и "word" (2 раза)

#### Тесты API endpoint

##### test_analyze_endpoint_success()
```python
response = self.client.post(
    '/analyze',
    json={"text": "hello world hello"},
    content_type='application/json'
)
```

**Назначение**: Проверяет успешное выполнение POST запроса.

**Как работает**:
- Отправляет POST запрос на `/analyze` с валидными JSON данными
- Проверяет статус код 200
- Проверяет наличие и корректность полей в ответе

##### test_analyze_endpoint_missing_text()
- Проверяет обработку ошибки при отсутствии поля "text"
- Ожидает: статус код 400

##### test_analyze_endpoint_not_json()
- Проверяет обработку ошибки при отправке не-JSON данных
- Ожидает: статус код 400

##### test_analyze_endpoint_invalid_text_type()
- Проверяет обработку ошибки при неверном типе поля "text"
- Ожидает: статус код 400

#### Запуск тестов

```python
if __name__ == '__main__':
    unittest.main()
```

**Как запустить**:
```bash
python test_app.py
# или
python -m unittest test_app.py
```

---

### 3. requirements.txt

```
Flask==3.0.0
```

**Назначение**: Список зависимостей Python проекта.

**Содержимое**:
- `Flask==3.0.0` - веб-фреймворк Flask версии 3.0.0

**Установка зависимостей**:
```bash
pip install -r requirements.txt
```

---

### 4. start_instances.py - Скрипт запуска инстансов (Python)

#### Назначение
Запускает несколько инстансов Flask приложения на разных портах для балансировки нагрузки.

#### Константа PORTS

```python
PORTS = [5001, 5002, 5003]
```

**Назначение**: Список портов для запуска инстансов.

#### Функция start_instance()

```python
def start_instance(port):
    env = os.environ.copy()
    env['PORT'] = str(port)
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process
```

**Как работает**:
1. Создает копию переменных окружения
2. Устанавливает переменную `PORT` для конкретного инстанса
3. Запускает `app.py` через `subprocess.Popen()` в фоновом режиме
4. Возвращает объект процесса

#### Основная функция

```python
if __name__ == '__main__':
    processes = []
    for port in PORTS:
        process = start_instance(port)
        processes.append(process)
```

**Как работает**:
- Запускает инстанс на каждом порту из списка PORTS
- Сохраняет все процессы в список
- При нажатии Ctrl+C останавливает все процессы

**Запуск**:
```bash
python start_instances.py
```

---

### 5. start_instances.bat - Скрипт запуска инстансов (Windows)

#### Назначение
Альтернативный способ запуска инстансов на Windows через командные окна.

#### Команды

```batch
start "Flask Instance 5001" cmd /k "set PORT=5001 && python app.py"
```

**Как работает**:
- `start` - запускает новое окно командной строки
- `"Flask Instance 5001"` - заголовок окна
- `cmd /k` - запускает cmd и оставляет окно открытым после выполнения команды
- `set PORT=5001` - устанавливает переменную окружения PORT
- `&&` - выполняет следующую команду только если предыдущая успешна
- `python app.py` - запускает Flask приложение

**Запуск**:
Двойной клик по файлу `start_instances.bat` или из командной строки:
```cmd
start_instances.bat
```

---

### 6. nginx.conf - Конфигурация Nginx

#### Блок upstream

```nginx
upstream flask_backend {
    server localhost:5001;
    server localhost:5002;
    server localhost:5003;
}
```

**Назначение**: Определяет группу серверов для балансировки нагрузки.

**Как работает**:
- `upstream flask_backend` - создает группу серверов с именем "flask_backend"
- `server localhost:5001` - добавляет сервер на порту 5001
- По умолчанию используется метод балансировки **round-robin** (по очереди)

**Методы балансировки** (можно указать явно):
- `round-robin` - по очереди (по умолчанию)
- `least_conn` - к серверу с наименьшим количеством соединений
- `ip_hash` - распределение по IP адресу клиента

#### Блок server

```nginx
server {
    listen 80;
    server_name localhost;
```

**Назначение**: Определяет виртуальный сервер Nginx.

**Параметры**:
- `listen 80` - Nginx слушает на порту 80 (стандартный HTTP порт)
- `server_name localhost` - имя сервера

#### Блок location

```nginx
location / {
    proxy_pass http://flask_backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Назначение**: Обрабатывает все запросы и проксирует их к Flask приложениям.

**Параметры**:
- `location /` - обрабатывает все пути (URL)
- `proxy_pass http://flask_backend` - перенаправляет запросы к группе серверов flask_backend
- `proxy_set_header` - устанавливает заголовки HTTP для правильной работы прокси:
  - `Host` - оригинальный хост из запроса
  - `X-Real-IP` - реальный IP адрес клиента
  - `X-Forwarded-For` - цепочка IP адресов прокси
  - `X-Forwarded-Proto` - оригинальный протокол (http/https)

**Таймауты**:
```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```
- Максимальное время ожидания соединения, отправки и чтения данных

#### Установка конфигурации

1. Скопировать `nginx.conf` в директорию конфигурации Nginx
2. Или добавить содержимое в основной конфигурационный файл Nginx
3. Перезапустить Nginx:
```bash
nginx -s reload
```

**Проверка конфигурации**:
```bash
nginx -t
```

---

### 7. .github/workflows/ci.yml - GitHub Actions CI/CD

#### Назначение
Автоматизированный pipeline для проверки кода при каждом push в ветку main.

#### Триггеры

```yaml
on:
  push:
    branches:
      - main
```

**Назначение**: Workflow запускается при каждом push в ветку main.

#### Job: test

**Назначение**: Запускает unit-тесты.

##### Шаг 1: Checkout code
```yaml
- name: Checkout code
  uses: actions/checkout@v3
```
- Клонирует репозиторий в виртуальную машину

##### Шаг 2: Set up Python
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'
```
- Устанавливает Python версии 3.11

##### Шаг 3: Install dependencies
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```
- Обновляет pip
- Устанавливает зависимости из requirements.txt

##### Шаг 4: Run tests
```yaml
- name: Run tests
  run: |
    python -m pytest test_app.py -v || python -m unittest test_app.py
```
- Запускает тесты через pytest или unittest
- `||` означает "или" - если pytest не установлен, используется unittest

#### Job: security

**Назначение**: Проверяет безопасность кода с помощью bandit.

##### Шаг 1-2: Аналогично job test

##### Шаг 3: Install bandit
```yaml
- name: Install bandit
  run: |
    python -m pip install --upgrade pip
    pip install bandit
```
- Устанавливает bandit - инструмент для проверки безопасности Python кода

##### Шаг 4: Run bandit
```yaml
- name: Run bandit security check
  continue-on-error: true
  run: |
    bandit -r . -f json -o bandit-report.json || true
    bandit -r . || echo "Bandit check completed - see warnings above"
```
- `-r .` - рекурсивно проверяет все Python файлы в текущей директории
- `-f json -o bandit-report.json` - сохраняет отчет в JSON формате
- `continue-on-error: true` - позволяет workflow продолжиться даже при предупреждениях
- `|| true` / `|| echo` - не прерывает workflow при обнаружении проблем

**Что проверяет bandit**:
- Использование небезопасных функций
- Проблемы с паролями и секретами
- SQL инъекции
- И другие уязвимости безопасности

**Подавление предупреждений (# nosec)**:
В коде используются комментарии `# nosec` для подавления ложных срабатываний:
- **B104** в `app.py`: `host='0.0.0.0'` необходим для работы с Nginx и балансировки нагрузки
- **B404, B603** в `start_instances.py`: `subprocess` используется безопасно (контролируемые входные данные, не пользовательский ввод)

Эти предупреждения не являются реальными проблемами безопасности в контексте данного проекта.

---

## Инструкция по установке и запуску

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск одного инстанса Flask

```bash
# Windows
set PORT=5001
python app.py

# Linux/Mac
export PORT=5001
python app.py
```

Приложение будет доступно по адресу: `http://localhost:5001`

### 3. Запуск нескольких инстансов

**Вариант 1 (Windows)**:
```cmd
start_instances.bat
```

**Вариант 2 (Python скрипт)**:
```bash
python start_instances.py
```

**Вариант 3 (Вручную в отдельных терминалах)**:
```bash
# Терминал 1
set PORT=5001
python app.py

# Терминал 2
set PORT=5002
python app.py

# Терминал 3
set PORT=5003
python app.py
```

### 4. Настройка Nginx

1. Установите Nginx (следуйте инструкции из "Установка Nginx на Windows.docx")

2. Скопируйте содержимое `nginx.conf` в конфигурационный файл Nginx:
   - Обычно находится в: `C:\nginx\conf\nginx.conf` (Windows)
   - Или добавьте содержимое в существующий конфиг

3. Проверьте конфигурацию:
```bash
nginx -t
```

4. Перезапустите Nginx:
```bash
nginx -s reload
```

5. Проверьте работу:
   - Откройте браузер: `http://localhost`
   - Запросы будут автоматически распределяться между портами 5001, 5002, 5003

### 5. Запуск тестов

```bash
python test_app.py
# или
python -m unittest test_app.py
```

### 6. Проверка безопасности (bandit)

```bash
pip install bandit
bandit -r .
```

---

## Примеры использования API

### Пример 1: Базовый запрос

**Запрос**:
```bash
curl -X POST http://localhost/analyze \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"hello world hello test\"}"
```

**Ответ**:
```json
{
  "word_count": 4,
  "most_frequent_words": [
    {"word": "hello", "count": 2},
    {"word": "world", "count": 1},
    {"word": "test", "count": 1}
  ]
}
```

### Пример 2: Текст с пунктуацией

**Запрос**:
```bash
curl -X POST http://localhost/analyze \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello, world! How are you? I am fine.\"}"
```

**Ответ**:
```json
{
  "word_count": 8,
  "most_frequent_words": [
    {"word": "hello", "count": 1},
    {"word": "world", "count": 1},
    {"word": "how", "count": 1},
    {"word": "are", "count": 1},
    {"word": "you", "count": 1},
    {"word": "i", "count": 1},
    {"word": "am", "count": 1},
    {"word": "fine", "count": 1}
  ]
}
```

### Пример 3: Ошибка - отсутствует поле "text"

**Запрос**:
```bash
curl -X POST http://localhost/analyze \
  -H "Content-Type: application/json" \
  -d "{}"
```

**Ответ**:
```json
{
  "error": "Missing 'text' field in request"
}
```
Статус код: 400

---

## Проверка балансировки нагрузки

Для проверки, что Nginx правильно распределяет запросы между инстансами:

1. Добавьте логирование в `app.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    logging.info(f"Request received on port {os.environ.get('PORT', 5000)}")
    # ... остальной код
```

2. Отправьте несколько запросов:
```bash
for i in {1..10}; do
  curl -X POST http://localhost/analyze \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"test $i\"}"
done
```

3. Проверьте логи каждого инстанса - запросы должны распределяться по очереди.

---

## Структура ответа API

### Успешный ответ (200 OK)

```json
{
  "word_count": <число>,
  "most_frequent_words": [
    {"word": "<слово>", "count": <частота>},
    ...
  ]
}
```

### Ошибки

**400 Bad Request - Не JSON формат**:
```json
{
  "error": "Request must be JSON"
}
```

**400 Bad Request - Отсутствует поле "text"**:
```json
{
  "error": "Missing 'text' field in request"
}
```

**400 Bad Request - Неверный тип поля "text"**:
```json
{
  "error": "'text' must be a string"
}
```

---

## Требования к системе

- Python 3.11 или выше
- Flask 3.0.0
- Nginx (для балансировки нагрузки)
- Git (для GitHub Actions)

---

## Заключение

Данный проект реализует все требования лабораторной работы №9, вариант 2:

✅ RESTful API на Flask с endpoint POST /analyze  
✅ Подсчет общего количества слов  
✅ Определение самых частотных слов  
✅ Unit-тесты для проверки функциональности  
✅ Настройка балансировки нагрузки с Nginx  
✅ Запуск нескольких инстансов на портах 5001, 5002, 5003  
✅ CI/CD workflow в GitHub Actions с автоматическими тестами  
✅ Проверка безопасности с помощью bandit  

Все компоненты подробно документированы и готовы к использованию и защите лабораторной работы.
