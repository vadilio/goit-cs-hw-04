import threading
import time
import os
from datetime import datetime

# Задані змінні
KEYWORDS = ["python", "async", "thread", "process", "performance"]
FILE_DIR = "text_files"
THREAD_COUNT = 4


def search_keywords_in_file(filepath, keywords):
    found_keywords = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for kw in keywords:
                if kw.lower() in content:
                    found_keywords.append(kw)
    except Exception as e:
        print(f"Помилка при обробці файлу {filepath}: {e}")
    return found_keywords


def worker(thread_id, files_subset, keywords, result_dict, lock):
    start_time = time.time()
    print(f"[{datetime.now()}] Потік {thread_id} почав роботу.")

    for file in files_subset:
        print(f"[{datetime.now()}] Потік {thread_id} обробляє файл: {file}")
        found = search_keywords_in_file(file, keywords)
        if found:
            with lock:
                for kw in found:
                    if kw not in result_dict:
                        result_dict[kw] = []
                    result_dict[kw].append(file)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{datetime.now()}] Потік {thread_id} завершив роботу. Час роботи: {elapsed:.4f} секунд.")


def multithreaded_search(files, keywords, num_threads=4):
    result_dict = {}
    lock = threading.Lock()

    chunk_size = (len(files) + num_threads - 1) // num_threads
    threads = []

    overall_start_time = time.time()
    print(f"[{datetime.now()}] Запуск пошуку у {num_threads} потоках...")

    for i in range(num_threads):
        subset = files[i*chunk_size: (i+1)*chunk_size]
        if not subset:
            continue
        t = threading.Thread(target=worker, args=(
            i+1, subset, keywords, result_dict, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    overall_end_time = time.time()
    overall_elapsed = overall_end_time - overall_start_time
    print(f"[{datetime.now()}] Всі потоки завершили роботу. Загальний час виконання: {overall_elapsed:.4f} секунд.")
    return result_dict


if __name__ == "__main__":
    if not os.path.isdir(FILE_DIR):
        print(f"Каталог '{FILE_DIR}' не знайдено.")
        exit(1)

    all_files = [os.path.join(FILE_DIR, f) for f in os.listdir(
        FILE_DIR) if os.path.isfile(os.path.join(FILE_DIR, f))]

    if not all_files:
        print(f"У каталозі '{FILE_DIR}' немає файлів.")
        exit(1)

    results = multithreaded_search(all_files, KEYWORDS, THREAD_COUNT)

    print("\nРезультати пошуку:")
    for kw, file_list in results.items():
        print(f"Ключове слово '{kw}' знайдено у файлах:")
        for file in file_list:
            print(f" - {file}")
