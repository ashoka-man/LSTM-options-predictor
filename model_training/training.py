import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam # SGD but not as stochastic

from torch.utils.data import DataLoader
#from torchvision import datasets, transforms

# Set device for training
device = (
    "cuda:0"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

print(f"Using {device} device")


# Define the hyperparameters
input_size = 7
