import numpy as np
from dataclasses import dataclass

@dataclass
class SimulationConfig:
    pass

class ArkheBraxSimulator:
    def __init__(self, scene="pendulum"):
        self.scene = scene

    def reset(self, seed=42):
        return {"x": np.random.randn(3).astype(np.float32), "qd": np.random.randn(6).astype(np.float32)}

    def step(self, state, action):
        return {"x": np.random.randn(3).astype(np.float32), "qd": np.random.randn(6).astype(np.float32)}

    def get_world_embedding(self, state):
        return np.random.randn(256).astype(np.float32)

    def get_trajectory_embedding(self, window=5):
        return np.random.randn(256).astype(np.float32)
