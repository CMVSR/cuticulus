"""Use transfer learning to train a model on ant image dataset."""

import numpy as np
import torch
from torch.utils.data import Dataset

from cuticulus.datasets import RoughSmoothFull


class TorchDS(Dataset):
    """Torch dataset class for ant image dataset."""

    def __init__(self, imgs: np.ndarray, labels: np.ndarray):
        """Initialize dataset.

        Args:
            imgs (np.ndarray): List of data.
            labels (np.ndarray): List of labels.
        """
        self.imgs = imgs
        self.labels = labels

    def __len__(self) -> int:
        """Return length of dataset.

        Returns:
            int: Length of dataset.
        """
        return len(self.imgs)

    def __getitem__(self, idx) -> tuple:
        """Return item at index idx.

        Returns:
            tuple: Tuple of image and label.
        """
        return self.imgs[idx], self.labels[idx]


samples = 500
size = (512, 512)
learning_rate = 0.001
ds = RoughSmoothFull(size)
ds.stratified_split(samples)
ds.split_validation()

train_x, train_y = ds.train()
test_x, test_y = ds.test()
valid_x, valid_y = ds.validate()
train_x = np.expand_dims(train_x, axis=1)
test_x = np.expand_dims(test_x, axis=1)

train_loader = torch.utils.data.DataLoader(
    dataset=TorchDS(train_x, train_y),
    batch_size=64,
    shuffle=True,
    num_workers=4,
)
test_loader = torch.utils.data.DataLoader(
    dataset=TorchDS(test_x, test_y),
    batch_size=64,
    shuffle=True,
    num_workers=4,
)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
for param in model.parameters():
    param.requires_grad = False

num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.fc.parameters(), lr=learning_rate)
model.to(device)

# train
for epoch in range(10):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(torch.device('cpu'))
        labels = labels.to(torch.device('cpu'))
        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

epochs = 1
steps = 0
running_loss = 0
print_every = 10
train_losses, test_losses = [], []
for epoch in range(epochs):
    for inputs, labels in train_loader:
        steps += 1
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        logps = model.forward(inputs)
        loss = criterion(logps, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

        if steps % print_every == 0:
            test_loss = 0
            accuracy = 0
            model.eval()
            with torch.no_grad():
                for inputs, labels in test_loader:
                    inputs, labels = inputs.to(device),
                    labels.to(device)
                    logps = model.forward(inputs)
                    batch_loss = criterion(logps, labels)
                    test_loss += batch_loss.item()

                    ps = torch.exp(logps)
                    top_p, top_class = ps.topk(1, dim=1)
                    equals = top_class == labels.view(*top_class.shape)
                    accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
            train_losses.append(running_loss/len(train_loader))
            test_losses.append(test_loss/len(test_loader))
            print(f"Epoch {epoch+1}/{epochs}.. "
                  f"Train loss: {running_loss/print_every:.3f}.. "
                  f"Test loss: {test_loss/len(test_loader):.3f}.. "
                  f"Test accuracy: {accuracy/len(test_loader):.3f}")
            running_loss = 0
            model.train()
torch.save(model, 'aerialmodel.pth')
