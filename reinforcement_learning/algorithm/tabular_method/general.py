import gym
import datetime
import argparse


def get_args():
    """
    """
    parser = argparse.ArgumentParser(description="hyperparameters")
    parser.add_argument('--algo_name', default='Q-learning', type=str, help="name of algorithm")
    parser.add_argument('--env_name', default='CliffWalking-v0', type=str, help="name of environment")
    parser.add_argument('--train_eps', default=1000, type=int, help="episodes of training")  # 训练的回合数
    parser.add_argument('--test_eps', default=20, type=int, help="episodes of testing")  # 测试的回合数
    parser.add_argument('--gamma', default=0.90, type=float, help="discounted factor")  # 折扣因子
    parser.add_argument('--epsilon_start', default=0.95, type=float,
                        help="initial value of epsilon")  # e-greedy策略中初始epsilon
    parser.add_argument('--epsilon_end', default=0.01, type=float,
                        help="final value of epsilon")  # e-greedy策略中的终止epsilon
    parser.add_argument('--epsilon_decay', default=300, type=int,
                        help="decay rate of epsilon")  # e-greedy策略中epsilon的衰减率
    parser.add_argument('--lr', default=0.1, type=float, help="learning rate")
    parser.add_argument('--device', default='cpu', type=str, help="cpu or gpu")
    args = parser.parse_args([])
    return args


def train(cfg, env, agent):
    print('开始训练！')
    print(f'环境:{cfg.env_name}, 算法:{cfg.algo_name}, 设备:{cfg.device}')
    rewards = []  # 记录奖励
    for i_ep in range(cfg.train_eps):
        ep_reward = 0  # 记录每个回合的奖励
        state = env.reset()  # 重置环境,即开始新的回合
        while True:
            action = agent.sample(state)  # 根据算法采样一个动作
            next_state, reward, done, _ = env.step(action)  # 与环境进行一次动作交互
            agent.learn(state, action, reward, next_state, done)  # Q学习算法更新
            state = next_state  # 更新状态
            ep_reward += reward
            if done:
                break
        rewards.append(ep_reward)
        if (i_ep + 1) % 20 == 0:
            print(f"回合：{i_ep + 1}/{cfg.train_eps}，奖励：{ep_reward:.1f}，Epsilon：{agent.epsilon:.3f}")
    print('完成训练！')
    return {"rewards": rewards}


def test(cfg, env, agent, render=False):
    print('开始测试！')
    print(f'环境：{cfg.env_name}, 算法：{cfg.algo_name}, 设备：{cfg.device}')
    rewards = []  # 记录所有回合的奖励
    for i_ep in range(cfg.test_eps):
        ep_reward = 0  # 记录每个episode的reward
        state = env.reset()  # 重置环境, 重新开一局（即开始新的一个回合）
        if render:
            env.render()
        while True:
            action = agent.predict(state)  # 根据算法选择一个动作
            next_state, reward, done, _ = env.step(action)  # 与环境进行一个交互
            if render:
                env.render()
            state = next_state  # 更新状态
            ep_reward += reward
            if done:
                break
        rewards.append(ep_reward)
        print(f"回合数：{i_ep + 1}/{cfg.test_eps}, 奖励：{ep_reward:.1f}")
    print('完成测试！')
    return {"rewards": rewards}


def env_agent_config(cfg, seed=1, algorithm=None):
    """
    创建环境和智能体
    """
    env = gym.make(cfg.env_name)
    env.seed(seed)  # 设置随机种子
    n_states = env.observation_space.n  # 状态维度
    n_actions = env.action_space.n  # 动作维度
    agent = algorithm(n_states, n_actions, cfg)
    return env, agent
