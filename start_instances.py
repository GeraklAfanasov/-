import subprocess
import sys
import os
import time

PORTS = [5001, 5002, 5003]

def start_instance(port):
    env = os.environ.copy()
    env['PORT'] = str(port)
    process = subprocess.Popen([sys.executable, 'app.py'], env=env)
    print(f"--> Инстанс на порту {port} запущен (PID: {process.pid})")
    return process

if __name__ == '__main__':
    processes = []
    try:
        for port in PORTS:
            processes.append(start_instance(port))
            time.sleep(1)
            
        print(f"\nВсе {len(processes)} инстанса работают. Нажмите Ctrl+C для выхода.\n")
        for p in processes:
            p.wait()
            
    except KeyboardInterrupt:
        print("\nОстановка процессов...")
        for p in processes:
            p.terminate()