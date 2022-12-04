import math
import random

import numpy as np
import paddle
import paddle.nn as nn
import paddle.nn.functional as F
import parl


class CartpoleModel(parl.Model):
    """ Linear network to solve Cartpole problem.
    Args:
        obs_dim (int): Dimension of observation space.
        act_dim (int): Dimension of action space.
    """

    def __init__(self, obs_dim, act_dim):
        super(CartpoleModel, self).__init__()
        hid1_size = 128
        hid2_size = 128
        self.fc1 = nn.Linear(obs_dim, hid1_size)
        self.fc2 = nn.Linear(hid1_size, hid2_size)
        self.fc3 = nn.Linear(hid2_size, act_dim)

    def forward(self, obs):
        h1 = F.relu(self.fc1(obs))
        h2 = F.relu(self.fc2(h1))
        Q = self.fc3(h2)
        return Q


class CartpoleAgent(parl.Agent):
    def __init__(self, algorithm, memory, cfg):
        super().__init__(algorithm)
        self.n_actions = cfg['n_actions']
        self.epsilon = cfg['epsilon_start']
        self.sample_count = 0
        self.epsilon_start = cfg['epsilon_start']
        self.epsilon_end = cfg['epsilon_end']
        self.epsilon_decay = cfg['epsilon_decay']
        self.batch_size = cfg['batch_size']
        self.global_step = 0
        self.update_target_steps = cfg['targe_update_fre']
        self.memory = memory

    def sample(self, obs):
        """Sample an action `for exploration` when given an observation
        Args:
            obs(np.float32): shape of (obs_dim,)
        Returns:
            act(int): action
        """
        self.sample_count += 1
        # epsilon must decay(linear,exponential and etc.) for balancing exploration and exploitation
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * \
                       math.exp(-1. * self.sample_count / self.epsilon_decay)
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.randint(self.n_actions)
        else:
            action = self.predict(obs)
        return action

    def predict(self, obs):
        """Predict an action when given an observation
        Args:
            obs(np.float32): shape of (obs_dim,)
        Returns:
            act(int): action
        """
        obs = paddle.to_tensor(obs, dtype='float32')
        pred_q = self.alg.predict(obs)
        act = np.argmax(pred_q.numpy())
        # print("act", act)
        return act

    def learn(self):
        """Update model with an episode data
        Returns:
            loss(float)
        """
        if len(self.memory) < self.batch_size:  # when transitions in memory do not meet a batch, not update
            return

        if self.global_step % self.update_target_steps == 0:
            self.alg.sync_target()
        self.global_step += 1
        state_batch, action_batch, reward_batch, next_state_batch, done_batch = self.memory.sample(self.batch_size)
        action_batch = np.expand_dims(action_batch, axis=-1)
        reward_batch = np.expand_dims(reward_batch, axis=-1)
        done_batch = np.expand_dims(done_batch, axis=-1)

        state_batch = paddle.to_tensor(state_batch, dtype='float32')
        action_batch = paddle.to_tensor(action_batch, dtype='int32')
        reward_batch = paddle.to_tensor(reward_batch, dtype='float32')
        next_state_batch = paddle.to_tensor(next_state_batch, dtype='float32')
        done_batch = paddle.to_tensor(done_batch, dtype='float32')
        loss = self.alg.learn(state_batch, action_batch, reward_batch, next_state_batch, done_batch)

        return float(loss)
