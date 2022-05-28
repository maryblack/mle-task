import unittest
from task_2.classification import MultiClassificator


class ClassificationTest(unittest.TestCase):
    def test_bicycle(self):
        self.assertEqual(MultiClassificator().predict("FAHRRAEDER // SPORTFAHRRAEDER"), "BICYCLES")


if __name__ == '__main__':
    unittest.main()