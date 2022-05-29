import unittest
from task_2.classification import MultiClassificator
import pandas as pd
from sklearn.metrics import accuracy_score


class ClassificationTest(unittest.TestCase):
    def test_bicycle(self):
        self.assertEqual(MultiClassificator().predict("FAHRRAEDER // SPORTFAHRRAEDER"), "BICYCLES")

    def test_usb(self):
        self.assertEqual(MultiClassificator().predict("LEEF IBRIDGE MOBILE SPEICHERERWEITERUNG FUER IPHONE, IPAD UND IPOD - MIT LIGHTNING UND USB, 128 GB"), "USB MEMORY")

    def test_accuracy(self):
        pred = MultiClassificator().eval_model(pd.read_csv("tests/testset.csv"))
        true = pd.read_csv("tests/testset_labels.csv")
        accuracy = accuracy_score(pred, true)
        self.assertGreater(accuracy, 0.9)


if __name__ == '__main__':
    unittest.main()