# Домашнее задание к лекции 1.7 «Классы и их применение в Python»
class Animal(object):
    def __init__(self, name, weight, voice):
        self.name = name
        self.weight = weight
        self.voice = voice

    def feed(self):
        # кормить
        print('feed', self.name)

    def voice(self):
        # различать по голосам(коровы мычат, утки крякают и т.д.)
        print('voice', self.name, self.voice)

    def product(self):
        raise NotImplementedError("Please Implement this method")


class Sheep(Animal):
    def __init__(self, name, weight):
        super().__init__(name, weight, 'ba-a-ba-a')

    def shear(self):
        # овец стричь
        print('shear', self.name)

    def product(self):
        self.shear()


class MilkAnimal(Animal):
    def milk(self):
        # корову и коз доить
        print('milk', self.name)

    def product(self):
        self.milk()


class Cow(MilkAnimal):
    def __init__(self, name, weight):
        super().__init__(name, weight, 'moo-moo')


class Goat(MilkAnimal):
    def __init__(self, name, weight):
        super().__init__(name, weight, 'ma-a-ma-a')


class Bird(Animal):
    def __init__(self, name, weight, voice):
        super().__init__(name, weight, voice)

    def egg(self):
        # собирать яйца у кур, утки и гусей
        print('egg', self.name)

    def product(self):
        self.egg()


class Goose(Bird):
    def __init__(self, name, weight):
        super().__init__(name, weight, 'honk-honk')


class Chicken(Bird):
    def __init__(self, name, weight):
        super().__init__(name, weight, 'cluck-cluck')


class Duck(Bird):
    def __init__(self, name, weight):
        super().__init__(name, weight, 'quack-quack')


# Для каждого животного из списка должен существовать экземпляр класса.
goose1 = Goose('Gray', 2.1)
goose2 = Goose('White', 2.2)
cow = Cow("Man'ka", 11.3)
sheep1 = Sheep('Barashek', 3.4)
sheep2 = Sheep('Curly', 3.5)
goat1 = Goat('Roga', 4.2)
goat2 = Goat('Kopyta', 4.3)
chicken1 = Chicken('Ko-Ko', 1.2)
chicken2 = Chicken('Kukareku', 1.5)
duck = Duck('Kryakva', 1.9)
animals = [goose1, goose2, cow, sheep1, sheep2, chicken1, chicken2, goat1, goat2, duck]

# Каждое животное требуется накормить и подоить/постричь/собрать яйца, если надо.
print('--feed animals')
for animal in animals:
    animal.feed()
print('--product animals')
for animal in animals:
    animal.product()

print('\n')
# Необходимо посчитать общий вес всех животных(экземпляров класса);
total_weight = 0
heaviest_animal = None
for animal in animals:
    total_weight = total_weight + animal.weight
print('Total weight', format(total_weight, '.2f'))

# Вывести название самого тяжелого животного.
for animal in animals:
    if heaviest_animal is None:
        heaviest_animal = animal
    elif animal.weight > heaviest_animal.weight:
        heaviest_animal = animal
print('The heaviest animal', heaviest_animal.name)
