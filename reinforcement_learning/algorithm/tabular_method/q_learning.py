import numpy as np

from reinforcement_learning.algorithm.tabular_method.tabular_method import TabularMethod


class QLearning(TabularMethod):
    def learn(self, state, action, reward, next_state, done):
        Q_predict = self.Q_table[str(state)][action]
        if done:  # 终止状态
            Q_target = reward
        else:
            Q_target = reward + self.gamma * np.max(self.Q_table[str(next_state)])
        self.Q_table[str(state)][action] += self.lr * (Q_target - Q_predict)
