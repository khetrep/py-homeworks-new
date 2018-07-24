# Задача №1
# нужно отыскать файл в формате sql среди десятков других,
# при этом вы знаете некоторые части этого файла (на память или из другого источника).
# Задача №2. Дополнительная (не обязательная)
# Генерировать абсолютный путь до папки с миграциями

import os
import mmap
import re


def list_sql_files_in_dir(target_dir):
    files = []
    for file in os.listdir(target_dir):
        if file.endswith(".sql"):
            files.append(os.path.join(target_dir, file))
    return files


def find_files_with_text(files, text):
    text_pattern = str.encode('(?i)'+text)
    filtered_files = []
    for file in files:
        with open(file, 'rb', 0) as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if re.search(text_pattern, s):
                filtered_files.append(file)
    return filtered_files


def main():
    migrations = 'Migrations'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, migrations)

    files = list_sql_files_in_dir(target_dir)
    while True:
        text = input('Введите текст для поиска. Для выхода используйте \"q\": ')
        if text.lower() == 'q':
            break
        files = find_files_with_text(files, text)
        for file in files:
            print(os.path.join(migrations, os.path.basename(file)))
        print("Найдено файлов: {}".format(len(files)))


if __name__ == "__main__":
    main()
