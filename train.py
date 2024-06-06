import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from model import NeuralNet
from nltk_utils import tokenize, stem, bag_of_words

# Load the intents file
with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

input_size = len(X_train[0])
hidden_size = 128
num_layers = 2  # Adding num_layers parameter
output_size = len(tags)
learning_rate = 0.001
num_epochs = 1000
batch_size = 8

model = NeuralNet(input_size, hidden_size, num_layers, output_size).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for i in range(0, len(X_train), batch_size):
        batch_X = X_train[i:i + batch_size]
        batch_y = y_train[i:i + batch_size]
        batch_X = torch.from_numpy(batch_X).float().unsqueeze(1)  # Adding a sequence length dimension
        batch_y = torch.from_numpy(batch_y).long()

        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

print('Training complete.')

# Save the model with the num_layers parameter
model_file = "data.pth"
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "num_layers": num_layers,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}
torch.save(data, model_file)
