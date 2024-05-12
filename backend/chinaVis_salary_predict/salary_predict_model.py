import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN_Salary_Predict(nn.Module):
    def __init__(self, input_size, output_size):
        super(CNN_Salary_Predict, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        linear_input_size = 32 * input_size
        self.fc1 = nn.Linear(linear_input_size, output_size * 2)
        self.fc2 = nn.Linear(output_size * 2, output_size)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 32 * self.input_size)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x
