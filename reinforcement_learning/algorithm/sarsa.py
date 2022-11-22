from reinforcement_learning.algorithm.template import TabularMethod


class Sarsa(TabularMethod):
    def update(self, state, action, reward, next_state, done):
        Q_predict = self.Q_table[str(state)][action]
        next_action = self.sample_action(next_state)
        if done:  # 终止状态
            Q_target = reward
        else:
            Q_target = reward + self.gamma * self.Q_table[str(next_state)][next_action]
        self.Q_table[str(state)][action] += self.lr * (Q_target - Q_predict)
