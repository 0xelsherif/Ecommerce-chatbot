import unittest
import torch
from torch.utils.data import DataLoader
from src.train import ChatDataset, NeuralNet

class TestTrain(unittest.TestCase):
    def test_dataset(self):
        dataset = ChatDataset()
        self.assertGreater(len(dataset), 0)

    def test_model_training(self):
        dataset = ChatDataset()
        train_loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True, num_workers=0)
        
        input_size = len(dataset.x_train[0])
        hidden_size = 8
        output_size = len(dataset.tags)
        model = NeuralNet(input_size, hidden_size, output_size)
        
        self.assertEqual(model.l1.in_features, input_size)
        self.assertEqual(model.l3.out_features, output_size)
        
        sample_data, sample_label = next(iter(train_loader))
        self.assertEqual(sample_data.shape[1], input_size)
        self.assertEqual(sample_label.shape[0], 8)

if __name__ == "__main__":
    unittest.main()
