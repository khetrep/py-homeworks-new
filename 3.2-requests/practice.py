"""
Необходимо расширить функцию переводчика так, чтобы она принимала следующие параметры:

Путь к файлу с текстом;
Путь к файлу с результатом;
Язык с которого перевести;
Язык на который перевести (по-умолчанию русский).
У вас есть 3 файла (DE.txt, ES.txt, FR.txt) с новостями на 3 языках: французском, испанском, немецком.
Функция должна взять каждый файл с текстом, перевести его на русский и сохранить результат в новом файле.

Для переводов можно пользоваться API Yandex.Переводчик.
"""
import requests
import os
from http import HTTPStatus

REQUEST_TIMEOUT = 60


def list_txt_files_in_dir(target_dir):
    files = []
    for file in os.listdir(target_dir):
        if file.endswith(".txt"):
            files.append(os.path.join(target_dir, file))
    return files


def ya_translate_file(text, lang_from, lang_to='ru'):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20180727T083645Z.7d690c2e7b45eee9.f4f26fc075811e2f49501003eb233303b746c747'
    params = {
        'key': key,
        'lang': lang_from + '-' + lang_to,
        'text': text,
    }
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    if response.status_code == HTTPStatus.OK:
        translated_text = ' '.join(response.json().get('text', []))
        return translated_text
    else:
        print('Failed translate: {}'.format(response.text))


def read_file(file):
    with open(file) as f:
        text = f.read()
    return text


def write_file(file, text):
    with open(file, 'w') as f:
        f.write(text)


def translate_file(file, file_out, lang, lang_to):
    print(f'start translate \"{file}\"')
    text = read_file(file)
    translated_text = ya_translate_file(text, lang, lang_to)
    if translated_text:
        write_file(file_out, translated_text)
        print(f'complete translate \"{file}\", write to \"{file_out}\"')


def main():
    lang_to = 'ru'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = list_txt_files_in_dir(current_dir)
    for file in files:
        lang = os.path.basename(file).lower()[:2]
        file_out = os.path.join(os.path.dirname(file), '{}.{}.txt'.format(lang.upper(), lang_to))
        translate_file(file, file_out, lang, lang_to)


if __name__ == "__main__":
    main()
