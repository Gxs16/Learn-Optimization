from abc import abstractmethod
from collections import defaultdict

import numpy as np


class TabularMethod:
    def __init__(self, n_states, n_actions, cfg):
        self.n_actions = n_actions
        self.lr = cfg.lr  # 学习率
        self.gamma = cfg.gamma
        self.epsilon = cfg.epsilon_start
        self.sample_count = 0
        self.epsilon_start = cfg.epsilon_start
        self.epsilon_end = cfg.epsilon_end
        self.epsilon_decay = cfg.epsilon_decay
        self.Q_table = defaultdict(lambda: np.zeros(n_actions))  # 用嵌套字典存放状态->动作->状态-动作值（Q值）的映射，即Q表

    @abstractmethod
    def sample_action(self, state):
        """
        采样动作，训练时用
        """

    @abstractmethod
    def predict_action(self, state):
        """
        预测或选择动作，测试时用
        """
        action = np.argmax(self.Q_table[str(state)])
        return action

    @abstractmethod
    def update(self, state, action, reward, next_state, done):
        pass
