"""Pytorch utilities."""

import time
from copy import deepcopy

import torch
import numpy as np

from cuticulus.console import console


class TorchDS(torch.utils.data.Dataset):
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


def train_model(
    model,
    dataloaders: dict,
    criterion: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    num_epochs=25,
):
    since = time.time()

    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }

    best_model_wts = deepcopy(model.state_dict())
    best_acc = float(0)

    for epoch in range(num_epochs):
        console.log('Epoch {0}/{1}'.format(epoch, num_epochs - 1))
        console.log('-' * 10)

        # Each epoch has a training and validation phase
        phases = ['train', 'val']
        for phase in phases:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = float(0)
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    # Get model outputs and calculate loss
                    # Special case for inception because in training it has an auxiliary output. In train
                    #   mode we calculate the loss by summing the final output and the auxiliary output
                    #   but in testing we only consider the final output.
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double(
            ) / len(dataloaders[phase].dataset)

            console.log('{0} Loss: {1:.4f} Acc: {2:.4f}'.format(
                phase,
                epoch_loss,
                epoch_acc,
            ))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = deepcopy(model.state_dict())

            if phase == 'train':
                history['train_acc'].append(epoch_acc)
                history['train_loss'].append(epoch_loss)
            elif phase == 'val':
                history['val_acc'].append(epoch_acc)
                history['val_loss'].append(epoch_loss)

    time_elapsed = time.time() - since
    console.log('Training complete in {0:.0f}m {1:.0f}s'.format(
        time_elapsed // 60,
        time_elapsed % 60,
    ))
    console.log('Best val Acc: {0:4f}'.format(
        best_acc,
    ))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, history


def test_model(model, dataloaders, criterion, device):
    running_loss = 0
    running_corrects = 0
    for inputs, labels in dataloaders:
        inputs = inputs.to(device)
        labels = labels.to(device)

        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)

    epoch_acc = running_corrects.double() / len(dataloaders.dataset)
    epoch_acc = epoch_acc.cpu().item()
    epoch_loss = running_loss / len(dataloaders.dataset)

    console.log('Loss: {0:.4f} Acc: {1:.4f}'.format(epoch_loss, epoch_acc))
    return epoch_acc, epoch_loss
