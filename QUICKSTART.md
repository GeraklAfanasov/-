# Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Запуск тестов

```bash
python test_app.py
```

## 3. Запуск одного инстанса Flask

```bash
# Windows
set PORT=5001
python app.py

# Linux/Mac
export PORT=5001
python app.py
```

## 4. Запуск нескольких инстансов (Windows)

Двойной клик на `start_instances.bat` или:

```cmd
start_instances.bat
```

## 5. Настройка Nginx

1. Скопируйте содержимое `nginx.conf` в конфигурационный файл Nginx
2. Проверьте конфигурацию: `nginx -t`
3. Перезапустите Nginx: `nginx -s reload`

## 6. Тестирование API

```bash
curl -X POST http://localhost/analyze -H "Content-Type: application/json" -d "{\"text\": \"hello world hello\"}"
```

Или через браузер используя расширение (например, Postman) или онлайн сервисы.

## 7. GitHub Actions

Workflow автоматически запустится при push в ветку `main`.

---

**Подробная документация**: см. `README.md`
