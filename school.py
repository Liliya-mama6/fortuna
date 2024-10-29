import unittest
import kontest
import logging



case=unittest.TestSuite()
case.addTest(unittest.TestLoader().loadTestsFromTestCase(kontest.RunnerTest))
text=unittest.TextTestRunner(verbosity=2)
text.run(case)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='runner_tes.log',
                        format='%(asctime)s | %(levelname)s | %('
                               'message)s', encoding='`UTF-8', filemode='w')

