import copy

import paddle
import parl


class DQN(parl.Algorithm):
    def __init__(self, model, gamma=None, lr=None):
        self.model = model
        self.target_model = copy.deepcopy(model)

        self.gamma = gamma
        self.lr = lr

        self.mse_loss = paddle.nn.MSELoss(reduction='mean')
        self.optimizer = paddle.optimizer.Adam(
            learning_rate=lr, parameters=self.model.parameters())

    def predict(self, obs):
        return self.model(obs)

    def learn(self, obs, action, reward, next_obs, terminal):
        # Q
        pred_values = self.model(obs)
        action_dim = pred_values.shape[-1]
        action = paddle.squeeze(action, axis=-1)
        action_onehot = paddle.nn.functional.one_hot(
            action, num_classes=action_dim)
        pred_value = pred_values * action_onehot
        pred_value = paddle.sum(pred_value, axis=1, keepdim=True)

        # target Q
        with paddle.no_grad():
            max_v = self.target_model(next_obs).max(1, keepdim=True)
            target = reward + (1 - terminal) * self.gamma * max_v
        loss = self.mse_loss(pred_value, target)

        # optimize
        self.optimizer.clear_grad()
        loss.backward()
        self.optimizer.step()
        return loss

    def sync_target(self):
        """ assign the parameters of the training network to the target network
        """
        self.model.sync_weights_to(self.target_model)
