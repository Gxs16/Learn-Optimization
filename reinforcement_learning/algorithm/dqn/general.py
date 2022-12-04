import argparse

import gym

from reinforcement_learning.algorithm.dqn.cartpole import CartpoleModel, CartpoleAgent
from reinforcement_learning.algorithm.dqn.deep_q_network import DQN
from reinforcement_learning.algorithm.dqn.replay_buffer import ReplayBuffer
from reinforcement_learning.utils.seed import all_seed


def get_args():
    """
    """
    parser = argparse.ArgumentParser(description="hyper parameters")
    parser.add_argument('--algo_name', default='DQN', type=str, help="name of algorithm")
    parser.add_argument('--env_name', default='CartPole-v0', type=str, help="name of environment")
    parser.add_argument('--train_eps', default=400, type=int, help="episodes of training")  # 训练的回合数
    parser.add_argument('--test_eps', default=20, type=int, help="episodes of testing")  # 测试的回合数
    parser.add_argument('--ep_max_steps', default=100000, type=int,
                        help="steps per episode, much larger value can simulate infinite steps")
    parser.add_argument('--gamma', default=0.99, type=float, help="discounted factor")  # 折扣因子
    parser.add_argument('--epsilon_start', default=0.95, type=float,
                        help="initial value of epsilon")  # e-greedy策略中初始epsilon
    parser.add_argument('--epsilon_end', default=0.01, type=float,
                        help="final value of epsilon")  # e-greedy策略中的终止epsilon
    parser.add_argument('--epsilon_decay', default=200, type=int,
                        help="decay rate of epsilon")  # e-greedy策略中epsilon的衰减率
    parser.add_argument('--memory_capacity', default=200000, type=int)  # replay memory的容量
    parser.add_argument('--memory_warmup_size', default=200, type=int)  # replay memory的预热容量
    parser.add_argument('--batch_size', default=64, type=int, help="batch size of training")  # 训练时每次使用的样本数
    parser.add_argument('--targe_update_fre', default=200, type=int,
                        help="frequency of target network update")  # target network更新频率
    parser.add_argument('--seed', default=0, type=int, help="seed")
    parser.add_argument('--lr', default=0.001, type=float, help="learning rate")
    parser.add_argument('--device', default='gpu', type=str, help="cpu or gpu")
    args = parser.parse_args([])
    args = {**vars(args)}  # type(dict)
    return args


def train(cfg, env, agent):
    """
    训练
    """
    print(f"开始训练！")
    print(f"环境：{cfg['env_name']}，算法：{cfg['algo_name']}，设备：{cfg['device']}")
    rewards = []  # record rewards for all episodes
    steps = []
    for i_ep in range(cfg["train_eps"]):
        ep_reward = 0  # reward per episode
        ep_step = 0
        state = env.reset()  # reset and obtain initial state
        for _ in range(cfg['ep_max_steps']):
            ep_step += 1
            action = agent.sample(state)  # sample action
            next_state, reward, done, _ = env.step(action)  # update env and return transitions
            agent.memory.push((state, action, reward, next_state, done))  # save transitions
            state = next_state  # update next state for env
            agent.learn()  # update agent
            ep_reward += reward  #
            if done:
                break
        steps.append(ep_step)
        rewards.append(ep_reward)
        if (i_ep + 1) % 10 == 0:
            print(f"回合：{i_ep + 1}/{cfg['train_eps']}，奖励：{ep_reward:.2f}，Epsilon: {agent.epsilon:.3f}")
    print("完成训练！")
    env.close()
    res_dic = {'episodes': range(len(rewards)), 'rewards': rewards, 'steps': steps}
    return res_dic


def test(cfg, env, agent):
    print("开始测试！")
    print(f"环境：{cfg['env_name']}，算法：{cfg['algo_name']}，设备：{cfg['device']}")
    rewards = []  # record rewards for all episodes
    steps = []
    for i_ep in range(cfg['test_eps']):
        ep_reward = 0  # reward per episode
        ep_step = 0
        state = env.reset()  # reset and obtain initial state
        for _ in range(cfg['ep_max_steps']):
            ep_step += 1
            action = agent.predict(state)  # predict action
            next_state, reward, done, _ = env.step(action)
            state = next_state
            ep_reward += reward
            if done:
                break
        steps.append(ep_step)
        rewards.append(ep_reward)
        print(f"回合：{i_ep + 1}/{cfg['test_eps']}，奖励：{ep_reward:.2f}")
    print("完成测试！")
    env.close()
    return {'episodes': range(len(rewards)), 'rewards': rewards, 'steps': steps}


def env_agent_config(cfg):
    """
    create env and agent
    """
    env = gym.make(cfg['env_name'])
    if cfg['seed'] != 0:  # set random seed
        all_seed(env, seed=cfg["seed"])
    n_states = env.observation_space.shape[0]  # print(hasattr(env.observation_space, 'n'))
    n_actions = env.action_space.n  # action dimension
    print(f"n_states: {n_states}, n_actions: {n_actions}")
    cfg.update({"n_states": n_states, "n_actions": n_actions})  # update to cfg parameters
    model = CartpoleModel(n_states, n_actions)
    algo = DQN(model, gamma=cfg['gamma'], lr=cfg['lr'])
    memory = ReplayBuffer(cfg["memory_capacity"])  # replay buffer
    agent = CartpoleAgent(algo, memory, cfg)  # create agent
    return env, agent
