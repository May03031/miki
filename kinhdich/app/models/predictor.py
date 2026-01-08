import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(1, 1)

    def forward(self, x):
        return self.fc(x)

class Predictor:
    def __init__(self):
        self.model = SimpleModel()
        self.model.eval()

    def predict(self, value: float) -> float:
        x = torch.tensor([[value]], dtype=torch.float32)
        y = self.model(x)
        return y.item()
