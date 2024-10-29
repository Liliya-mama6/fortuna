import logging
import urban
import unittest


class RunnerTest(unittest.TestCase):

    def test_walk(self):
        try:
            a = urban.Runner('turtle', speed=-3)
            for i in range(10):
                a.walk()
            self.assertEqual(a.distance, 50)
            logging.info('"test_walk" выполнен успешно')
        except ValueError as err:
            logging.warning('Неверная скорость для Runner', exc_info=True)

    def test_run(self):
        try:
            a = urban.Runner('kkk')
            for i in range(10):
                a.run()
            self.assertEqual(a.distance, 100)
        except:
            logging.warning('Неверный тип данных для объекта Runner', exc_info=True)

    def test_challenge(self):
        a = urban.Runner('pomidurov')
        b = urban.Runner('oguchok')
        for i in range(10):
            a.run()
            b.walk()
        self.assertNotEqual(a.distance, b.distance)


