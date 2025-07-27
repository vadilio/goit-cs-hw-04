import os
import random
from faker import Faker

FILE_DIR = "text_files"
KEYWORDS = ["python", "async", "thread", "process", "performance"]
NUM_FILES = 5  # кількість файлів
WORDS_PER_FILE = 800  # кількість слів у кожному файлі

fake = Faker()

os.makedirs(FILE_DIR, exist_ok=True)


def generate_text_with_keywords(word_count, keywords):
    # Генеруємо "word_count" слів випадкового тексту
    words = fake.words(nb=word_count, unique=False)

    # Вставляємо 1-2 ключових слова у випадкові позиції
    num_keywords = random.randint(1, 2)
    for _ in range(num_keywords):
        kw = random.choice(keywords)
        pos = random.randint(0, len(words))
        words.insert(pos, kw)
    return " ".join(words)


for i in range(1, NUM_FILES + 1):
    filename = f"file_{i}.txt"
    filepath = os.path.join(FILE_DIR, filename)
    text = generate_text_with_keywords(WORDS_PER_FILE, KEYWORDS)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

print(
    f"Згенеровано {NUM_FILES} файлів по {WORDS_PER_FILE} слів кожен у папці '{FILE_DIR}'")
