from reinforcement_learning.utils.plot import plot_rewards
from reinforcement_learning.algorithm.dqn.general import test, train, env_agent_config, get_args

def main():
    cfg = get_args()
    # 训练
    env, agent = env_agent_config(cfg)
    res_dic = train(cfg, env, agent)

    plot_rewards(res_dic['rewards'], cfg)
    # 测试
    res_dic = test(cfg, env, agent)
    plot_rewards(res_dic['rewards'], cfg)


if __name__ == '__main__':
    main()
    # print(envs.registry.all())