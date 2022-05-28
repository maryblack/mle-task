import unittest
from task_2.classification import MultiClassificator


class ClassificationTest(unittest.TestCase):
    def test_bicycle(self):
        self.assertEqual(MultiClassificator().predict("FAHRRAEDER // SPORTFAHRRAEDER"), "BICYCLES")

    def test_usb(self):
        self.assertEqual(MultiClassificator().predict("LEEF IBRIDGE MOBILE SPEICHERERWEITERUNG FUER IPHONE, IPAD UND IPOD - MIT LIGHTNING UND USB, 128 GB"), "USB MEMORY")


if __name__ == '__main__':
    unittest.main()