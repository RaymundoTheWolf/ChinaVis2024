from torch.nn import TransformerEncoder, TransformerEncoderLayer
import torch.nn as nn
import torch.nn.functional as F


class CNN_Salary_Predict(nn.Module):
    def __init__(self, input_size, output_size):
        super(CNN_Salary_Predict, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv1_bn = nn.BatchNorm1d(16)  # 添加批归一化层
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv2_bn = nn.BatchNorm1d(32)  # 添加批归一化层
        linear_input_size = 32 * input_size
        self.fc1 = nn.Linear(linear_input_size, output_size * 2)
        self.fc2 = nn.Linear(output_size * 2, output_size)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = F.relu(self.conv1_bn(self.conv1(x)))  # 应用批归一化层
        x = F.relu(self.conv2_bn(self.conv2(x)))  # 应用批归一化层
        x = x.view(-1, 32 * self.input_size)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x


class RNN_Salary_Predict(nn.Module):
    def __init__(self, input_size, output_size):
        super(RNN_Salary_Predict, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.rnn = nn.RNN(input_size=input_size, hidden_size=256, num_layers=3, batch_first=True)
        self.fc1 = nn.Linear(256, output_size * 2)
        self.fc2 = nn.Linear(output_size * 2, output_size)

    def forward(self, x):
        x = x.unsqueeze(dim=1)
        out, _ = self.rnn(x)
        out = out.squeeze()
        out = self.fc1(out)
        out = F.relu(out)
        out = self.fc2(out)
        return out


class Transformer_Salary_Predict(nn.Module):
    def __init__(self, input_size, output_size):
        super(Transformer_Salary_Predict, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.encoder_layers = TransformerEncoderLayer(d_model=input_size, nhead=1)
        self.transformer_encoder = TransformerEncoder(self.encoder_layers, num_layers=2)
        self.fc1 = nn.Linear(input_size, output_size * 2)
        self.fc2 = nn.Linear(output_size * 2, output_size)

    def forward(self, x):
        x = x.unsqueeze(dim=1)
        x = x.permute(1, 0, 2)
        out = self.transformer_encoder(x)
        out = out[-1]
        out = self.fc1(out)
        out = F.relu(out)
        out = self.fc2(out)
        return out
