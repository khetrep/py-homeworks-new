# Домашнее задание к лекции 1.2-1.3 «Циклы. Типы данных. Коллекции данных»

# 1.Понимание типов данных.
# dictionary
request = {
  'method': 'GET',
  'accept-encoding': 'gzip',
  'referer': 'https://www.google.com/',
  'upgrade-insecure-requests': 1
}
# set
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# tuple
country = ('RU', 'RUS', 'Russia')
# list
countries = {
  ('ru', 'Russia'),
  ('SE', 'SWE', 'Sweden'),
  ('KR', 'KOR', 'South Korea')
}

# 2.Пользуясь знаниями, научитесь отображать различную информацию из массива данных по квартирам и попробуйте поработать с множествами и словарями

import csv


flats_list = list()

with open('output.csv', newline='') as csvfile:
	flats_csv = csv.reader(csvfile, delimiter=';')
	flats_list = list(flats_csv)

flats_list.pop(0)

#можете посмотреть содержимое файла с квартирами через print, можете - на вкладке output.csv
#print (flats_list)


#TODO 1:
# 1) Напишите цикл, который проходит по всем квартирам, и показывает только новостройки
#и их порядковые номера в файле. Подсказка - вам нужно изменить этот код:
print('Новостройки:')
new_flat_count = 0
for idx, flat in enumerate(flats_list):
  if "новостройка" in flat:
    new_flat_count += 1
    print("{}) {}".format(idx, flat))
# 2) добавьте в код подсчет количества новостроек
print("Количество новостроек: {}".format(new_flat_count));


#TODO 2:
# 1) Сделайте описание квартиры в виде словаря, а не списка. Используйте следующие поля из файла output.csv: ID, Количество комнат;Новостройка/вторичка, Цена (руб). У вас должно получиться примерно так:
flat_info = {"id":flat[0], "rooms":flat[1], "type":flat[2], "price":flat[11]}

flats_dict = {}
for flat in flats_list:
  flats_dict[flat[0]] = {
    "id":flat[0],
    "rooms":flat[1],
    "type":flat[2],
    "price":flat[11]
  }
print('Квартиры в виде словаря:')
print(flats_dict)

# 2) Измените код, который создавал словарь для поиска квартир по метро так, чтобы значением словаря был не список ID квартир, а список описаний квартир в виде словаря, который вы сделали в п.1
subway_dict = {}
for flat in flats_list:
  subway = flat[3].replace("м.", "")
  if subway not in subway_dict.keys():
    subway_dict[subway] = list()
  subway_dict[subway].append(flats_dict[flat[0]])
print('Словарь для поиска квартир по метро:')
print(subway_dict)

# 3) Самостоятельно напишите код, который подсчитываети выводит, сколько квартир нашлось у каждого метро.
print('Сколько квартир нашлось у каждого метро:')
for subway, subway_flats  in subway_dict.items():
  print('Метро \"{}\" кол-во {}'.format(subway, len(subway_flats)))