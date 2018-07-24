# Задача №3. Вызов других программ
# Нужно написать программу для запуска браузера.
import subprocess


def main():
    browser = 'chromium-browser'
    subprocess.run(args=[browser, 'https://netology.ru/programs/python'])


if __name__ == "__main__":
    main()
