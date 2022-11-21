import math

import numpy as np

from reinforcement_learning.algorithm.template import TabularMethod


class QLearning(TabularMethod):
    def sample_action(self, state):
        self.sample_count += 1
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * math.exp(
            -1. * self.sample_count / self.epsilon_decay)  # epsilon是会递减的，这里选择指数递减

        # e-greedy 策略
        if np.random.uniform(0, 1) > self.epsilon:
            action = np.argmax(self.Q_table[str(state)])  # 选择Q(s,a)最大对应的动作
        else:
            action = np.random.choice(self.n_actions)  # 随机选择动作
        return action

    def predict_action(self, state):
        action = np.argmax(self.Q_table[str(state)])
        return action

    def update(self, state, action, reward, next_state, done):
        Q_predict = self.Q_table[str(state)][action]
        if done:  # 终止状态
            Q_target = reward
        else:
            Q_target = reward + self.gamma * np.max(self.Q_table[str(next_state)])
        self.Q_table[str(state)][action] += self.lr * (Q_target - Q_predict)
