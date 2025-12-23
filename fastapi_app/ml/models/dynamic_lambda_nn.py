"""
NetPredict Dynamic λ(t) Neural Network
Replaces rule-based λ later without touching simulation.
"""

import torch
import torch.nn as nn

class DynamicLambdaNet(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Softplus()
        )

    def forward(self, x):
        return self.net(x)