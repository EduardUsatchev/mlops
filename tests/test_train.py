import unittest
from src.train import train_model

class TestTrainModel(unittest.TestCase):
    def test_train_output(self):
        mse = train_model()
        self.assertTrue(mse > 0, "MSE should be greater than 0")

if __name__ == '__main__':
    unittest.main()
