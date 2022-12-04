from reinforcement_learning.algorithm.tabular_method.tabular_method import TabularMethod


class Sarsa(TabularMethod):
    def learn(self, state, action, reward, next_state, done):
        Q_predict = self.Q_table[str(state)][action]
        next_action = self.sample(next_state)
        if done:  # 终止状态
            Q_target = reward
        else:
            Q_target = reward + self.gamma * self.Q_table[str(next_state)][next_action]
        self.Q_table[str(state)][action] += self.lr * (Q_target - Q_predict)
