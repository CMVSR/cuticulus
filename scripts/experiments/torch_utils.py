"""Utility functions for torch experiments."""

import copy
import time

import numpy as np
import torch

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

        Args:
            idx (int): Index of item.

        Returns:
            tuple: Tuple of image and label.
        """
        return self.imgs[idx], self.labels[idx]


def inception_loss(
    model: torch.nn.Module,
    inputs: torch.Tensor,
    labels: torch.Tensor,
    criterion,
) -> tuple[torch.Tensor, float]:
    """Calculate inception loss.

    Args:
        model (torch.nn.Module): Model to calculate inception loss for.
        inputs (torch.Tensor): Inputs to calculate inception loss for.
        labels (torch.Tensor): Labels for inputs.
        criterion (torch.nn.modules.loss._Loss): Loss function.

    Returns:
        tuple[torch.Tensor, float]: Tuple of outputs and loss.
    """
    outputs, aux_outputs = model(inputs)
    loss1 = criterion(outputs, labels)
    loss2 = criterion(aux_outputs, labels)
    inception_param = 0.4
    loss = loss1 + inception_param * loss2
    return outputs, loss


def train_step(
    model: torch.nn.Module,
    phase: str,
    inputs: torch.Tensor,
    labels: torch.Tensor,
    criterion: torch.nn.modules.loss._Loss,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    is_inception: bool = False,
) -> tuple[float, int]:
    """One iteration of training.

    Args:
        model (torch.nn.Module): Model to train.
        phase (str): Phase to train for ('train' or 'val').
        inputs (torch.Tensor): Inputs to train on.
        labels (torch.Tensor): Labels for inputs.
        criterion (torch.nn.modules.loss._Loss): Loss function.
        optimizer (torch.optim.Optimizer): Optimizer to use.
        device (torch.device): Device to use.
        is_inception (bool): Whether to use inception loss.

    Returns:
        tuple[float, int]: Tuple of loss and number of correct predictions.
    """
    # Iterate over data.
    inputs = inputs.to(device)
    labels = labels.to(device)

    # zero the parameter gradients
    optimizer.zero_grad()

    # forward
    # track history if only in train
    with torch.set_grad_enabled(phase == 'train'):
        if is_inception and phase == 'train':
            outputs, loss = inception_loss(
                model, inputs, labels, criterion,
            )
        else:
            outputs = model(inputs)
            loss = criterion(outputs, labels)

        _, preds = torch.max(outputs, 1)

        # backward + optimize only if in training phase
        if phase == 'train':
            loss.backward()
            optimizer.step()

    # statistics
    loss = loss.item() * inputs.size(0)
    corrects = torch.sum(preds == labels.data)
    return loss, corrects


def train_model(
    model: torch.nn.Module,
    dataloaders: dict,
    criterion,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    num_epochs: int = 25,
    is_inception: bool = False,
) -> tuple[torch.nn.Module, dict]:
    """Train model.

    Args:
        model (torch.nn.Module): Model to train.
        dataloaders (dict): Dataloaders for training and validation.
        criterion (_type_): Loss function.
        optimizer (torch.optim.Optimizer): Optimizer to use.
        device (torch.device): Device to use.
        num_epochs (int): Number of epochs to train for.
        is_inception (bool): Whether to use inception loss.

    Returns:
        tuple[torch.nn.Module, dict]: Tuple of trained model and training
        history.
    """
    start = time.time()

    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
    }

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = float(0)

    for epoch in range(num_epochs):
        console.log('Epoch {0}/{1}'.format(epoch, num_epochs - 1))
        console.log('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ('train', 'val'):
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = float(0)
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                loss, corrects = train_step(
                    model,
                    phase,
                    inputs,
                    labels,
                    criterion,
                    optimizer,
                    device,
                    is_inception,
                )
                running_loss += loss
                running_corrects += corrects

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double(
            ) / len(dataloaders[phase].dataset)

            console.log('{0} Loss: {1:.4f} Acc: {2:.4f}'.format(
                phase, epoch_loss, epoch_acc,
            ))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

            if phase == 'train':
                history['train_acc'].append(epoch_acc)
                history['train_loss'].append(epoch_loss)
            elif phase == 'val':
                history['val_acc'].append(epoch_acc)
                history['val_loss'].append(epoch_loss)

    time_elapsed = time.time() - start
    console.log('Training complete in {0:.0f}m {1:.0f}s'.format(
        time_elapsed // 60,
        time_elapsed % 60,
    ))
    console.log('Best val Acc: {0:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, history
