from reinforcement_learning.utils.plot import plot_rewards
from utils.general import test, train, env_agent_config, get_args
from algorithm.sarsa import Sarsa
from algorithm.q_learning import QLearning


def main():
    cfg = get_args()
    # 训练
    env, agent = env_agent_config(cfg, 1, QLearning)
    res_dic = train(cfg, env, agent)

    plot_rewards(res_dic['rewards'], cfg)
    # 测试
    res_dic = test(cfg, env, agent, True)
    plot_rewards(res_dic['rewards'], cfg)


if __name__ == '__main__':
    main()
    # print(envs.registry.all())