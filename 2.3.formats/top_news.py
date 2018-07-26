import collections
import json
import os
from pprint import pprint

import chardet


def list_json_files_in_dir(target_dir):
    files = []
    for file in os.listdir(target_dir):
        if file.endswith(".json"):
            files.append(os.path.join(target_dir, file))
    return files


def index_line(words, line, min_word_len=6):
    for word in list(filter(lambda x: len(x) > min_word_len, line.split())):
        if word in words:
            words[word] += 1
        else:
            words[word] = 1


def index_file(file, top_count=10, min_word_len=6):
    with open(file, 'rb') as f:
        raw_data = b''.join([f.readline() for _ in range(20)])
        encoding = chardet.detect(raw_data)['encoding']
    words = {}
    with open(file, encoding=encoding) as f:
        items = json.load(f)["rss"]["channel"]["items"]
        for item in items:
            index_line(words, item['description'], min_word_len)
            index_line(words, item['title'], min_word_len)

    sorted_words = sorted(words.items(), key=lambda kv: kv[1], reverse=True)
    top_words = collections.Counter(sorted_words).most_common(top_count)
    return top_words


def main():
    files_dir = "PY1_Lesson_2.3"
    top_count = 10

    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, files_dir)
    files = list_json_files_in_dir(target_dir)
    for file in files:
        top_words = index_file(file, top_count, 6)
        print("Top {} words in file \"{}\":".format(top_count, os.path.basename(file)))
        pprint(top_words)


if __name__ == "__main__":
    main()
