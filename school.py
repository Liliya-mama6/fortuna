import queue
from threading import Thread
from random import randint
from time import sleep
from queue import Queue


class Table:
    def __init__(self, number):
        self.guest = None
        self.number = number


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        t = randint(3, 10)
        sleep(t)


class Cafe:
    def __init__(self, *tables):
        self.tables = [i for i in tables]
        self.q = Queue()
        self.stol_zanyat = [0 for i in tables]

    def guest_arrival(self, *guests):
        for i in range(len(guests)):
            a = True
            if 0 not in self.stol_zanyat:
                print(f"{guests[i].name} в очереди")
                self.q.put(guests[i])
            for j in range(len(self.tables)):
                if a and self.tables[j].guest is None:
                    print(f"{guests[i].name} сел(-а) за стол номер {self.tables[j].number}")
                    guests[i].start()
                    a = False
                    self.tables[j].guest = guests[i]
                    self.stol_zanyat[i] = 1

    def discuss_guests(self):
        while 1 in self.stol_zanyat or not self.q.empty():
            for i in range(len(self.tables)):
                if self.stol_zanyat[i] == 1 and not self.tables[i].guest is None and not self.tables[i].guest.is_alive():
                    print(f"{self.tables[i].guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {self.tables[i].number} своlбоден")
                    self.tables[i].guest = None
                    self.stol_zanyat[i] = 0
                    if not self.q.empty():
                        k = self.q.get()
                        k.start()
                        self.tables[i].guest = k
                        print(f'{self.tables[i].guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {self.tables[i].number}')
                        self.stol_zanyat[i] = 1


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
