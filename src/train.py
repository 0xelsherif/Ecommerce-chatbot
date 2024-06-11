import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from preprocess import tokenize, stem, bag_of_words, load_intents

class ChatDataset(Dataset):
    def __init__(self):
        self.intents = load_intents('data/intents.json')
        self.all_words = []
        self.tags = []
        self.xy = []
        for intent in self.intents['intents']:
            tag = intent['tag']
            self.tags.append(tag)
            for pattern in intent['patterns']:
                w = tokenize(pattern)
                self.all_words.extend(w)
                self.xy.append((w, tag))
        self.ignore_words = ['?', '!', '.', ',']
        self.all_words = [stem(w) for w in self.all_words if w not in self.ignore_words]
        self.all_words = sorted(set(self.all_words))
        self.tags = sorted(set(self.tags))
        
        self.x_train = []
        self.y_train = []
        for (pattern_sentence, tag) in self.xy:
            bag = bag_of_words(pattern_sentence, self.all_words)
            self.x_train.append(bag)
            label = self.tags.index(tag)
            self.y_train.append(label)
        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)

    def __getitem__(self, index):
        return self.x_train[index], self.y_train[index]

    def __len__(self):
        return len(self.x_train)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out

if __name__ == "__main__":
    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True, num_workers=0)

    input_size = len(dataset.x_train[0])
    hidden_size = 8
    output_size = len(dataset.tags)
    learning_rate = 0.001
    num_epochs = 1000

    model = NeuralNet(input_size, hidden_size, output_size)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(torch.float32)
            labels = labels.to(torch.long)

            outputs = model(words)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    print('Training complete.')
    torch.save({
        'input_size': input_size,
        'hidden_size': hidden_size,
        'output_size': output_size,
        'model_state': model.state_dict(),
        'all_words': dataset.all_words,
        'tags': dataset.tags
    }, "models/chatbot_model.pth")
