@echo off
REM Скрипт для запуска нескольких инстансов Flask приложения на Windows
REM Запускает Flask приложения на портах 5001, 5002, 5003 в отдельных окнах

echo Запуск инстансов Flask приложения...

REM Запускаем первый инстанс на порту 5001 в новом окне
start "Flask Instance 5001" cmd /k "set PORT=5001 && python app.py"

REM Запускаем второй инстанс на порту 5002 в новом окне
start "Flask Instance 5002" cmd /k "set PORT=5002 && python app.py"

REM Запускаем третий инстанс на порту 5003 в новом окне
start "Flask Instance 5003" cmd /k "set PORT=5003 && python app.py"

echo Все инстансы запущены. Закройте окна для остановки.
