"""
Скрипт для запуска нескольких инстансов Flask приложения на разных портах.
Это необходимо для настройки балансировки нагрузки с помощью Nginx.
"""
import subprocess  # nosec B404
import sys
import os

# Порты, на которых будут запущены инстансы Flask приложения
PORTS = [5001, 5002, 5003]


def start_instance(port):
    """
    Запускает один инстанс Flask приложения на указанном порту.
    
    Args:
        port (int): Номер порта для запуска приложения
    """
    # Устанавливаем переменную окружения PORT для Flask приложения
    env = os.environ.copy()
    env['PORT'] = str(port)
    
    # Запускаем Flask приложение через Python
    # Используем subprocess.Popen для запуска в фоновом режиме
    # Входные данные контролируются (порты из константы, не пользовательский ввод)
    process = subprocess.Popen(  # nosec B603
        [sys.executable, 'app.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"Запущен инстанс Flask на порту {port} (PID: {process.pid})")
    return process


if __name__ == '__main__':
    """
    Основная функция для запуска всех инстансов.
    """
    processes = []
    
    try:
        # Запускаем инстанс на каждом порту
        for port in PORTS:
            process = start_instance(port)
            processes.append(process)
        
        print(f"\nЗапущено {len(processes)} инстансов Flask приложения.")
        print("Нажмите Ctrl+C для остановки всех инстансов.\n")
        
        # Ожидаем завершения (или прерывания пользователем)
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        # При нажатии Ctrl+C останавливаем все процессы
        print("\nОстановка всех инстансов...")
        for process in processes:
            process.terminate()
        print("Все инстансы остановлены.")
