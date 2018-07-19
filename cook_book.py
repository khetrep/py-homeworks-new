# Читать список рецептов из этого файла.
import pprint


def read_dish(f):
    ingridient_count = int(f.readline().strip())
    current_cook = []
    for r in range(ingridient_count):
        ingridient = f.readline().strip().split('|')
        current_cook.append({
            'ingridient_name': ingridient[0].strip(),
            'quantity': int(ingridient[1].strip()),
            'measure': ingridient[2].strip()
        })
    return current_cook


def read_cook_book(filename):
    cooks = {}
    with open(filename) as f:
        while True:
            dish = f.readline().strip()
            if dish == '':
                break
            cooks[dish] = read_dish(f)
            f.readline()
    return cooks


def add_ingridient_to_shop_list(shop_list, ingridient):
    name = ingridient['ingridient_name']
    if name not in shop_list:
        shop_list[name] = {
            'measure': ingridient['measure'],
            'quantity': ingridient['quantity']
        }
    else:
        shop_list[name]['quantity'] += ingridient['quantity']


def get_shop_list_by_dishes(cook_book, dishes, person_count):
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
            add_ingridient_to_shop_list(shop_list, ingridient)
    for name, ingridient in shop_list.items():
        ingridient['quantity'] *= person_count
    return shop_list


def main():
    pp = pprint.PrettyPrinter(indent=2)

    cook_book = read_cook_book('cook_book.txt')
    print('Кулинарная книга')
    pp.pprint(cook_book)

    print('\n')

    shop_list_2 = get_shop_list_by_dishes(cook_book, ['Запеченный картофель', 'Омлет'], 2)
    print('Необходимые ингридиенты')
    pp.pprint(shop_list_2)


if __name__ == "__main__":
    main()