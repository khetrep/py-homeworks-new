# Задача №4. Дополнительная (не обязательная)
# Есть программа (Image Magick для Windows и Linux, либо встроенная утилиту sips для mac),
# которая сжимает фотографии, и есть папка «Source» с самими фотографиями.
# Каждую фотографию мы хотим уменьшить до 200px в ширину (высота меняется пропорционально).
# Нужно для каждой фотографии запустить программу и результат работы положить в папку «Result»
import os
import subprocess


def list_files_in_dir(target_dir):
    files = []
    for file in os.listdir(target_dir):
        files.append(os.path.join(target_dir, file))
    return files


def main():
    source_dir = 'Source'
    result_dir = 'Result'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_abs_dir = os.path.join(current_dir, source_dir)
    result_abs_dir = os.path.join(current_dir, result_dir)
    if not os.path.exists(result_abs_dir):
        os.makedirs(result_abs_dir)

    source_files = list_files_in_dir(source_abs_dir)

    for file in source_files:
        output_file = os.path.join(result_abs_dir, os.path.basename(file))
        subprocess.run(args=['convert', file, '-resize', '200', output_file], check=True)
        print(output_file)


if __name__ == "__main__":
    main()
