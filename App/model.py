import os
import gdown
import numpy as np
import timm
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
from tqdm import tqdm



train_dataset = None
test_dataset = None
valid_dataset = None


for root, dirs, files in os.walk('cats_and_dogs'):
    for dir in dirs:
        if dir == "train":
            train_dataset = os.path.join(root, dir)
        elif dir == 'valid':
            valid_dataset = os.path.join(root, dir)
        elif dir == 'test':
            test_dataset = os.path.join(root, dir)


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=True, num_classes=2)

# preparing data

train_data = datasets.ImageFolder(train_dataset, transform=transform)
val_data = datasets.ImageFolder(valid_dataset, transform=transform)


train_loader = DataLoader(train_data, batch_size=8, shuffle=True)
val_loader = DataLoader(val_data, batch_size=8, shuffle=True)

# train The model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device=device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(10):
    model.train()
    total_loss = 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        tqdm.write(f'Epoch : {epoch+1} Total Loss: {total_loss/len(train_loader)}')
    print(f'Epoch {epoch+1}')

torch.save(model.state_dict(), 'swin_model.pth')
