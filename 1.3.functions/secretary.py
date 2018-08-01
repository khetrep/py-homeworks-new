"""
Задача №1
Необходимо реализовать пользовательские команды, которые будут выполнять следующие функции:

p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит
l – list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин"
s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится
a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца
 и номер полки, на котором он будет храниться.
Внимание: p, s, l, a - это пользовательские команды, а не названия функций. Функции должны иметь выразительное
 название, передающие её действие.
"""
HELP = 'p(people) – спросить номер документа и выведет имя человека, которому он принадлежит\n' \
       'l(list) – вывести список всех документов в формате passport "2207 876234" "Василий Гупкин"\n' \
       's(shelf) – спросить номер документа и выведет номер полки, на которой он находится\n' \
       'a(add) – добавить новый документ в каталог и в перечень полок,спросив его номер,тип,имя владельца\n'


def find_document_by_number(documents):
    # команда, которая спросит номер документа и выведет имя человека, которому он принадлежит
    number = input('Поиск владельца документа по номеру. Введите номер документа:')
    for document in documents:
        if document['number'] == number:
            print('Владелец документа с номером \"{}\": \"{}\"'.format(number, document.get('name')))
            return
    print('Документ с номером \"{}\" не найден'.format(number))


def list_all_documents(documents):
    # команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин"
    print('Cписок всех документов(type, number, name):')
    for document in documents:
        print('{} \"{}\" \"{}\"'.format(document['type'], document['number'], document['name']))


def find_shelf_document_by_number(documents, directories):
    # команда, которая спросит номер документа и выведет номер полки, на которой он находится
    number = input('Поиск номера полки, на которой находится документ. Введите номер документа:')
    for document in documents:
        if document['number'] == number:
            for k, shelf in directories.items():
                if number in shelf:
                    print('Номер полки с документом \"{}\": \"{}\"'.format(number, k))
                    return
            print('Полка с документом \"{}\" не найдена'.format(number))
            return
    print('Документ с номером \"{}\" не найден'.format(number))


def add_new_document(documents, directories):
    # команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца
    # и номер полки, на котором он будет храниться.
    number = input('Введите номер документа:')
    if not number:
        print('Ошибка! Номер документа не может быть пустым')
        return
    document_type = input('Введите тип документа:')
    if not document_type:
        print('Ошибка! Тип документа не может быть пустым')
        return
    name = input('Введите имя владельца документа:')
    if not name:
        print('Ошибка! Имя владельца документа не может быть пустым')
        return
    directory = input('Введите номер полки, где будет храниться документ:')
    if not directory:
        print('Ошибка! Номер полки не может быть пустым')
        return
    documents.append({
        "type": document_type,
        "number": number,
        "name": name
    })
    document_dir = directories.get(directory)
    if not document_dir:
        directories[directory] = [number]
    else:
        directories[directory].append(number)


def command_help():
    print(HELP)


def register_commands(commands, documents, directories):
    commands['p'] = lambda: find_document_by_number(documents)
    commands['l'] = lambda: list_all_documents(documents)
    commands['s'] = lambda: find_shelf_document_by_number(documents, directories)
    commands['a'] = lambda: add_new_document(documents, directories)


def wait_commands(commands):
    while True:
        text = input('Введите команду. Справка \"h\". Для выхода используйте \"q\": ')
        if not text:
            continue
        if text.lower() == 'q':
            break
        cmd = commands.get(text.lower())
        if not cmd:
            command_help()
        else:
            cmd()


def main():
    documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        {"type": "passport", "number": "900", "name": "Антон Чехов"}
    ]
    directories = {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': []
    }
    commands = {}
    register_commands(commands, documents, directories)
    wait_commands(commands)


if __name__ == "__main__":
    main()
