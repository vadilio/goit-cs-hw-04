import multiprocessing
import time
import os
from datetime import datetime

KEYWORDS = ["python", "async", "thread", "process", "performance"]
FILE_DIR = "text_files"
PROCESS_COUNT = 4


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


def worker(proc_id, files_subset, keywords, queue):
    start_time = time.time()
    print(f"[{datetime.now()}] Процес {proc_id} почав роботу.")

    local_result = {}

    for file in files_subset:
        print(f"[{datetime.now()}] Процес {proc_id} обробляє файл: {file}")
        found = search_keywords_in_file(file, keywords)
        if found:
            for kw in found:
                if kw not in local_result:
                    local_result[kw] = []
                local_result[kw].append(file)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{datetime.now()}] Процес {proc_id} завершив роботу. Час роботи: {elapsed:.4f} секунд.")

    # Відправляємо локальний результат у чергу
    queue.put(local_result)


def multiprocess_search(files, keywords, num_processes=4):
    chunk_size = (len(files) + num_processes - 1) // num_processes
    processes = []
    queue = multiprocessing.Queue()

    overall_start_time = time.time()
    print(f"[{datetime.now()}] Запуск пошуку у {num_processes} процесах...")

    for i in range(num_processes):
        subset = files[i*chunk_size: (i+1)*chunk_size]
        if not subset:
            continue
        p = multiprocessing.Process(
            target=worker, args=(i+1, subset, keywords, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    overall_end_time = time.time()
    overall_elapsed = overall_end_time - overall_start_time
    print(f"[{datetime.now()}] Всі процеси завершили роботу. Загальний час виконання: {overall_elapsed:.4f} секунд.")

    # Збираємо результати з усіх процесів
    combined_results = {}
    while not queue.empty():
        local_result = queue.get()
        for kw, files_list in local_result.items():
            if kw not in combined_results:
                combined_results[kw] = []
            combined_results[kw].extend(files_list)

    # Унікалізуємо списки файлів
    for kw in combined_results:
        combined_results[kw] = list(set(combined_results[kw]))

    return combined_results


if __name__ == "__main__":
    if not os.path.isdir(FILE_DIR):
        print(f"Каталог '{FILE_DIR}' не знайдено.")
        exit(1)

    all_files = [os.path.join(FILE_DIR, f) for f in os.listdir(
        FILE_DIR) if os.path.isfile(os.path.join(FILE_DIR, f))]

    if not all_files:
        print(f"У каталозі '{FILE_DIR}' немає файлів.")
        exit(1)

    results = multiprocess_search(all_files, KEYWORDS, PROCESS_COUNT)

    print("\nРезультати пошуку:")
    for kw, file_list in results.items():
        print(f"Ключове слово '{kw}' знайдено у файлах:")
        for file in file_list:
            print(f" - {file}")
