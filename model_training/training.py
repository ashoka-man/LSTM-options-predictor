import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam # SGD but not as stochastic

from torch.utils.data import DataLoader
#from torchvision import datasets, transforms

class OptionsPredictionLSTM(nn.Module):
    def __init__(self, input_size, hidden_layers_size, num_layers):
        super().__init__()

        # Setting hyperparameters to dictate input tensor shape
        self.input_size = input_size
        self.hidden_layers_size = hidden_layers_size
        self.num_layers = num_layers

        # Set device for training
        self.device = (
            "cuda:0"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        # Define the LSTM
        self.lstm = nn.LSTM(input_size, hidden_layers_size, num_layers, batch_first = True)

        # Define the connections between layers
        self.fc = nn.Linear(hidden_layers_size, 1)

    def forward(self, input_tensor):
        # Find the batch_size
        batch_size = input_tensor.size()[0]
        # Initialize the hidden and cell state
        h_0 = torch.zeros(num_layers, batch_size, self.hidden_layers_size).to(self.device)
        c_0 = torch.zeros(num_layers, batch_size, self.hidden_layers_size).to(self.device)

        # Run through the LSTM and take the output from the last time step in each sequence
        out, _ = self.lstm(input_tensor, (h_0, c_0))
        out = self.fc(out[:, -1, :])

        return out

# Define the hyperparameters
input_size = 7
hidden_layers_size = 200
num_layers = 1
output_size = 1
learning_rate = 0.01 # May have to change this later or find some optimal rate

