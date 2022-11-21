import matplotlib.pyplot as plt
import seaborn as sns


def smooth(data: list, weight: float = 0.9) -> list:
    """用于平滑曲线，类似于Tensorboard中的smooth

    Args:
        data:输入数据
        weight: 平滑权重，处于0-1之间，数值越高说明越平滑，一般取0.9

    Returns:
        smoothed: 平滑后的数据
    """
    last = data[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in data:
        smoothed_val = last * weight + (1 - weight) * point  # 计算平滑值
        smoothed.append(smoothed_val)
        last = smoothed_val
    return smoothed


def plot_rewards(rewards, cfg):
    sns.set()
    plt.figure()  # 创建一个图形实例，方便同时多画几个图
    plt.title("learning curve on {} of {} for {}".format(
        cfg.device, cfg.algo_name, cfg.env_name))
    plt.xlabel('epsiodes')
    plt.plot(rewards, label='rewards')
    plt.plot(smooth(rewards), label='smoothed')
    plt.legend()
    plt.show()
