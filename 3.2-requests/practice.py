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


def translate_file(file, file_out, lang_from, lang_to='ru'):
    print('start translate \"{}\"'.format(file))
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20180727T083645Z.7d690c2e7b45eee9.f4f26fc075811e2f49501003eb233303b746c747'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_abs = os.path.join(current_dir, file)
    file_out_abs = os.path.join(current_dir, file_out)

    with open(file_abs) as f:
        text = f.read()

    params = {
        'key': key,
        'lang': lang_from + '-' + lang_to,
        'text': text,
    }

    timeout = 60
    response = requests.get(url, params=params, timeout=timeout)
    # print(response.text)
    translated_text = ' '.join(response.json().get('text', []))
    with open(file_out_abs, 'w') as f:
        f.write(translated_text)
    print('complete translate \"{}\", write to \"{}\"'.format(file, file_out))
    return translated_text


def main():
    lang_to = 'ru'
    for file in ['DE.txt', 'ES.txt', 'FR.txt']:
        lang = file.lower()[:2]
        translate_file(file, '{}.{}.txt'.format(lang.upper(), lang_to), lang, lang_to)


if __name__ == "__main__":
    main()
